# view/login_window.py
# OOP Concept: Class, Encapsulation, GUI Layout Split Design

import tkinter as tk
from tkinter import messagebox, simpledialog
from StudentAttendanceTracker.controller.auth_controller import AuthController
from StudentAttendanceTracker.utils.security import Security
from StudentAttendanceTracker.model.database import Database
from StudentAttendanceTracker.view.admin_dashboard import AdminDashboard
from StudentAttendanceTracker.view.instructor_dashboard import InstructorDashboard

class LoginWindow:
    """Login Window with Modern Split Left-Right Design."""

    def __init__(self, root):
        """Initialize the Login Window."""
        self.root = root
        self.root.title("Student Attendance Tracker - Login")
        self.auth = AuthController()

        # Set window size
        self.root.geometry("850x500")
        self.root.resizable(False, False)

        # Left Side Frame (Light Background)
        self.left_frame = tk.Frame(root, bg="#dbe0e6", width=400)
        self.left_frame.pack(side="left", fill="both")

        # Right Side Frame (Dark Background)
        self.right_frame = tk.Frame(root, bg="#2e2e2e", width=450)
        self.right_frame.pack(side="right", fill="both")

        # Left Frame Content
        tk.Label(self.left_frame, text="STUDENT\nATTENDANCE\nTRACKER",
                 bg="#dbe0e6", fg="#1d1d1d",
                 font=("Arial", 28, "bold"), justify="center").place(relx=0.5, rely=0.4, anchor="center")

        tk.Label(self.left_frame, text="Designed & Developed by:\nSarabjeet Singh\nSukhmanpreet Kaur\nVaibhav Atulkumar Purohit",
                 bg="#dbe0e6", fg="#1d1d1d", font=("Arial", 9), justify="center").place(relx=0.5, rely=0.8, anchor="center")

        # Right Frame Content (Login Form)
        tk.Label(self.right_frame, text="LOGIN", bg="#2e2e2e", fg="white",
                 font=("Arial", 28, "bold")).place(relx=0.5, rely=0.2, anchor="center")

        # Username Label and Entry
        tk.Label(self.right_frame, text="Username", bg="#2e2e2e", fg="white",
                 font=("Arial", 12)).place(relx=0.3, rely=0.35, anchor="center")
        self.username_entry = tk.Entry(self.right_frame, font=("Arial", 12), width=25)
        self.username_entry.place(relx=0.7, rely=0.35, anchor="center")

        # Password Label and Entry
        tk.Label(self.right_frame, text="Password", bg="#2e2e2e", fg="white",
                 font=("Arial", 12)).place(relx=0.3, rely=0.45, anchor="center")
        self.password_entry = tk.Entry(self.right_frame, font=("Arial", 12), width=25, show="*")
        self.password_entry.place(relx=0.7, rely=0.45, anchor="center")

        # Error Message Label
        self.error_label = tk.Label(self.right_frame, text="", bg="#2e2e2e", fg="red", font=("Arial", 10, "bold"))
        self.error_label.place(relx=0.5, rely=0.52, anchor="center")

        # Login Button
        tk.Button(self.right_frame, text="LOGIN", font=("Arial", 12, "bold"),
                  width=20, bg="white", fg="#2e2e2e", command=self.login).place(relx=0.5, rely=0.62, anchor="center")

        # Register Button (Admin Only)
        tk.Button(self.right_frame, text="Register Admin", font=("Arial", 10),
                  width=20, bg="#4d4d4d", fg="white", command=self.register_admin).place(relx=0.5, rely=0.7, anchor="center")

    def login(self):
        """Authenticate user and open appropriate dashboard."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.auth.login(username, password)

        if role:
            self.error_label.config(text="")
            messagebox.showinfo("Login Success", f"Welcome {role}!")
            self.root.destroy()

            dashboard_root = tk.Tk()
            if role == "Admin":
                AdminDashboard(dashboard_root, username)
            elif role == "Instructor":
                InstructorDashboard(dashboard_root, username)
            else:
                messagebox.showerror("Login Error", "Unknown role detected!")
                dashboard_root.destroy()

            dashboard_root.mainloop()
        else:
            self.error_label.config(text="WRONG USERNAME OR PASSWORD!!!")

    def register_admin(self):
        """Open Admin Registration Form."""
        register_root = tk.Toplevel(self.root)
        register_root.title("Register Admin")
        register_root.geometry("500x400")
        register_root.resizable(False, False)

        frame = tk.Frame(register_root, padx=20, pady=20, bd=2, relief=tk.GROOVE)
        frame.pack(padx=50, pady=50)

        tk.Label(frame, text="Register New Admin", font=("Arial", 20, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(frame, text="Username:", font=("Arial", 12)).grid(row=1, column=0, sticky="e", pady=10)
        username_entry = tk.Entry(frame, font=("Arial", 12), width=25)
        username_entry.grid(row=1, column=1, pady=10)

        tk.Label(frame, text="Password:", font=("Arial", 12)).grid(row=2, column=0, sticky="e", pady=10)
        password_entry = tk.Entry(frame, font=("Arial", 12), width=25, show="*")
        password_entry.grid(row=2, column=1, pady=10)

        confirm_label = tk.Label(frame, text="Confirm Password:", font=("Arial", 12))
        confirm_label.grid(row=3, column=0, sticky="e", pady=10)
        confirm_entry = tk.Entry(frame, font=("Arial", 12), width=25, show="*")
        confirm_entry.grid(row=3, column=1, pady=10)

        message_label = tk.Label(frame, text="", font=("Arial", 10))
        message_label.grid(row=4, column=0, columnspan=2, pady=5)

        def register_action():
            """Register new admin."""
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            confirm = confirm_entry.get().strip()

            if not username or not password or not confirm:
                message_label.config(text="Fill all fields!", fg="red")
                return

            if password != confirm:
                message_label.config(text="Passwords do not match!", fg="red")
                return

            db = Database()
            db.connect()
            cursor = db.connection.cursor()

            try:
                # Check if user exists
                cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
                if cursor.fetchone():
                    message_label.config(text="Username already exists!", fg="red")
                    return

                hashed_password = Security.hash_password(password)
                hashed_password = hashed_password.decode('utf-8')

                cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                               (username, hashed_password, "Admin"))
                db.connection.commit()
                message_label.config(text="Admin registered successfully!", fg="green")

                username_entry.delete(0, tk.END)
                password_entry.delete(0, tk.END)
                confirm_entry.delete(0, tk.END)

            except Exception as e:
                message_label.config(text=f"Error: {e}", fg="red")
            finally:
                db.close()

        tk.Button(frame, text="Register", font=("Arial", 12),
                  width=20, command=register_action).grid(row=5, column=0, columnspan=2, pady=20)
