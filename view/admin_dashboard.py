# view/admin_dashboard.py
# OOP Concept: Class, Encapsulation, Dynamic Modern Admin Panel

import tkinter as tk
import csv
import tkinter.ttk as ttk
from tkinter import messagebox
from StudentAttendanceTracker.model.database import Database
from StudentAttendanceTracker.utils.security import Security


class AdminDashboard:
    """Full Admin Dashboard - Professional Modern Layout."""

    def __init__(self, root, username):
        """Initialize Admin Dashboard."""
        self.root = root
        self.username = username
        self.root.title("Admin Dashboard - Student Attendance Tracker")

        self.root.geometry("1150x700")
        self.root.resizable(False, False)

        # Set Background
        self.root.configure(bg="#2e2e2e")

        # Top Welcome Bar
        self.create_top_bar()

        # Left Sidebar
        self.sidebar = tk.Frame(self.root, width=270, bg="#2e2e2e")
        self.sidebar.pack(side="left", fill="y")

        # Right Main Content
        self.main_content = tk.Frame(self.root, bg="#f0f0f0")
        self.main_content.pack(expand=True, fill="both")

        # Sidebar Buttons
        self.add_sidebar_buttons()

        self.is_dark_mode = False
        self.apply_theme()
        self.show_dashboard_overview()

    def create_top_bar(self):
        """Create top welcome bar."""
        welcome_bar = tk.Frame(self.root, height=40, bg="#dbe0e6")
        welcome_bar.pack(side="top", fill="x")
        tk.Label(welcome_bar, text=f"Welcome, {self.username} 🎓",
                 font=("Arial", 14, "bold"),
                 bg="#dbe0e6", fg="#2e2e2e", anchor="w", padx=20).pack(fill="both")

    def add_sidebar_buttons(self):
        """Create Sidebar Buttons."""
        button_settings = {"font": ("Arial", 12, "bold"), "width": 22, "height": 2, "bg": "#dbe0e6", "fg": "#2e2e2e", "bd": 0}

        self.dashboard_btn = tk.Button(self.sidebar, text="🎯 Dashboard", command=self.show_dashboard_overview,
                                       **button_settings)
        self.dashboard_btn.pack(pady=10, padx=10)

        self.instructors_btn = tk.Button(self.sidebar, text="👩‍🏫 Manage Instructors", command=self.show_manage_instructors, **button_settings)
        self.instructors_btn.pack(pady=10, padx=10)

        self.students_btn = tk.Button(self.sidebar, text="🎓 Manage Students", command=self.show_manage_students, **button_settings)
        self.students_btn.pack(pady=10, padx=10)

        self.reports_btn = tk.Button(self.sidebar, text="📄 View Reports", command=self.show_view_reports, **button_settings)
        self.reports_btn.pack(pady=10, padx=10)

        self.class_btn = tk.Button(self.sidebar, text="🏫 Manage Class", command=self.show_manage_class, **button_settings)
        self.class_btn.pack(pady=10, padx=10)

        self.profile_btn = tk.Button(self.sidebar, text="⚙️ Admin Profile", command=self.show_admin_profile, **button_settings)
        self.profile_btn.pack(pady=10, padx=10)

        self.theme_btn = tk.Button(self.sidebar, text="🌗 Toggle Theme", command=self.toggle_theme, **button_settings)
        self.theme_btn.pack(pady=10, padx=10)

        self.logout_btn = tk.Button(self.sidebar, text="🔒 Logout", command=self.logout,
                                    font=("Arial", 12, "bold"), width=22, height=2, bg="red", fg="white", bd=0)
        self.logout_btn.pack(pady=20, padx=10)

    def clear_main_content(self):
        """Clear the Main Content."""
        for widget in self.main_content.winfo_children():
            widget.destroy()

    # -------------------------- Pages --------------------------

    def show_dashboard_overview(self):
        """Show Admin Dashboard Overview with Stats."""
        self.clear_main_content()

        tk.Label(self.main_content, text="Welcome to Dashboard 🎯", font=("Arial", 22, "bold"),
                 bg="#f0f0f0", fg="#2e2e2e").pack(pady=30)

        stats_frame = tk.Frame(self.main_content, bg="#f0f0f0")
        stats_frame.pack(pady=10, padx=20)

        # Fetch statistics
        total_students = self.get_total_students()
        total_instructors = self.get_total_instructors()
        total_classes = self.get_total_classes()
        total_attendance = self.get_total_attendance()

        cards = [
            ("🎓 Total Students", total_students),
            ("👩‍🏫 Total Instructors", total_instructors),
            ("🏫 Total Classes", total_classes),
            ("📄 Attendance Records", total_attendance)
        ]

        for idx, (title, count) in enumerate(cards):
            card = tk.Frame(stats_frame, bg="#dbe0e6", width=200, height=150, bd=2, relief="ridge")
            card.grid(row=0, column=idx, padx=20)

            tk.Label(card, text=title, font=("Arial", 12, "bold"), bg="#dbe0e6", fg="#2e2e2e").pack(pady=10)
            tk.Label(card, text=str(count), font=("Arial", 24, "bold"), bg="#dbe0e6", fg="#2e2e2e").pack()

    def get_total_students(self):
        db = Database()
        db.connect()
        cursor = db.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM students")
        result = cursor.fetchone()[0]
        db.close()
        return result

    def get_total_instructors(self):
        db = Database()
        db.connect()
        cursor = db.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM instructors")
        result = cursor.fetchone()[0]
        db.close()
        return result

    def get_total_classes(self):
        db = Database()
        db.connect()
        cursor = db.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM classes")
        result = cursor.fetchone()[0]
        db.close()
        return result

    def get_total_attendance(self):
        db = Database()
        db.connect()
        cursor = db.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM attendance")
        result = cursor.fetchone()[0]
        db.close()
        return result

    def show_manage_instructors(self):
        """Manage Instructors Form and List."""
        self.clear_main_content()

        tk.Label(self.main_content, text="Manage Instructors 👩‍🏫", font=("Arial", 20, "bold"),
                 bg="#f0f0f0", fg="#2e2e2e").pack(pady=20)

        container = tk.Frame(self.main_content, bg="#f0f0f0")
        container.pack(expand=True, fill="both", padx=20)

        # Left Form
        form_frame = tk.Frame(container, bg="#f0f0f0")
        form_frame.pack(side="left", fill="y", padx=20)

        self.inst_name_var = tk.StringVar()
        self.inst_id_var = tk.StringVar()
        self.inst_email_var = tk.StringVar()
        self.inst_dept_var = tk.StringVar()

        # Instructor Name
        tk.Label(form_frame, text="Instructor Name:", font=("Arial", 12), bg="#f0f0f0", fg="#2e2e2e").pack(pady=5,
                                                                                                           anchor="w")
        tk.Entry(form_frame, textvariable=self.inst_name_var, font=("Arial", 12), width=25).pack(pady=5)

        # Instructor ID
        tk.Label(form_frame, text="Instructor ID:", font=("Arial", 12), bg="#f0f0f0", fg="#2e2e2e").pack(pady=5,
                                                                                                         anchor="w")
        tk.Entry(form_frame, textvariable=self.inst_id_var, font=("Arial", 12), width=25).pack(pady=5)

        # Email
        tk.Label(form_frame, text="Email:", font=("Arial", 12), bg="#f0f0f0", fg="#2e2e2e").pack(pady=5, anchor="w")
        tk.Entry(form_frame, textvariable=self.inst_email_var, font=("Arial", 12), width=25).pack(pady=5)

        # Department (as Dropdown Combobox)
        tk.Label(form_frame, text="Department:", font=("Arial", 12), bg="#f0f0f0", fg="#2e2e2e").pack(pady=5,
                                                                                                      anchor="w")
        import tkinter.ttk as ttk
        self.inst_dept_combobox = ttk.Combobox(form_frame, textvariable=self.inst_dept_var, font=("Arial", 12),
                                               width=22, state="readonly")
        self.inst_dept_combobox.pack(pady=5)

        # Form Buttons
        tk.Button(form_frame, text="➕ Add Instructor", width=20, font=("Arial", 12),
                  bg="#dbe0e6", fg="#2e2e2e", command=self.add_instructor).pack(pady=10)
        tk.Button(form_frame, text="✏️ Edit Instructor", width=20, font=("Arial", 12),
                  bg="#dbe0e6", fg="#2e2e2e", command=self.edit_instructor).pack(pady=10)
        tk.Button(form_frame, text="🗑️ Delete Instructor", width=20, font=("Arial", 12),
                  bg="#dbe0e6", fg="#2e2e2e", command=self.delete_instructor).pack(pady=10)
        tk.Button(form_frame, text="📋 View All Instructors", width=20, font=("Arial", 12),
                  bg="#dbe0e6", fg="#2e2e2e", command=self.view_all_instructors).pack(pady=10)

        # Right List
        list_frame = tk.Frame(container, bg="#f0f0f0")
        list_frame.pack(side="right", expand=True, fill="both")

        tk.Label(list_frame, text="Instructor List 📚", font=("Arial", 14, "bold"),
                 bg="#f0f0f0", fg="#2e2e2e").pack(pady=10)

        self.instructor_listbox = tk.Listbox(list_frame, font=("Arial", 12), bg="white", fg="#2e2e2e", height=20,
                                             width=50)
        self.instructor_listbox.pack(padx=10, pady=10, expand=True, fill="both")

        self.instructor_listbox.bind("<<ListboxSelect>>", self.load_instructor_to_form)

        # Load data
        self.load_departments_for_instructors()
        self.load_instructors()

    def load_departments_for_instructors(self):
        """Load available Departments from Class table into combobox."""
        db = Database()
        db.connect()
        cursor = db.connection.cursor()

        cursor.execute("SELECT class_name FROM classes ORDER BY class_name ASC")
        departments = [row[0] for row in cursor.fetchall()]
        self.inst_dept_combobox["values"] = departments

        db.close()

    def view_all_instructors(self):
        """Show All Instructors neatly with 4 columns inside main content."""
        self.clear_main_content()

        tk.Label(self.main_content, text="All Instructors 📋", font=("Arial", 20, "bold"),
                 bg="#f0f0f0", fg="#2e2e2e").pack(pady=20)

        table_frame = tk.Frame(self.main_content, bg="#f0f0f0")
        table_frame.pack(expand=True, fill="both", padx=20)

        # Column Headers
        headers = ["Instructor ID", "Instructor Name", "Instructor Email", "Instructor Department"]
        for idx, header in enumerate(headers):
            tk.Label(table_frame, text=header, font=("Arial", 12, "bold"),
                     bg="#dbe0e6", fg="#2e2e2e", width=20, relief="groove").grid(row=0, column=idx, padx=1, pady=1)

        # Fetch Instructor Data
        db = Database()
        db.connect()
        cursor = db.connection.cursor()

        cursor.execute("SELECT instructor_id, name, email, department FROM instructors")
        instructors = cursor.fetchall()

        # Display Rows
        for row_idx, instructor in enumerate(instructors, start=1):
            for col_idx, value in enumerate(instructor):
                tk.Label(table_frame, text=value if value else "-", font=("Arial", 12),
                         bg="white", fg="#2e2e2e", width=20, relief="ridge").grid(row=row_idx, column=col_idx, padx=1,
                                                                                  pady=1)

        db.close()

        # Back Button
        tk.Button(self.main_content, text="🔙 Back to Manage Instructors", font=("Arial", 12, "bold"),
                  width=30, bg="#dbe0e6", fg="#2e2e2e", command=self.show_manage_instructors).pack(pady=20)

    def load_instructors(self):
        """Load instructors into listbox."""
        self.instructor_listbox.delete(0, tk.END)
        db = Database()
        db.connect()
        cursor = db.connection.cursor()

        cursor.execute("SELECT name, instructor_id FROM instructors")
        for row in cursor.fetchall():
            self.instructor_listbox.insert(tk.END, f"{row[0]} ({row[1]})")

        db.close()

    def load_instructor_to_form(self, event):
        """Load selected instructor to form."""
        selected = self.instructor_listbox.curselection()
        if selected:
            item = self.instructor_listbox.get(selected[0])
            name_part, id_part = item.rsplit("(", 1)
            inst_id = id_part.replace(")", "").strip()

            db = Database()
            db.connect()
            cursor = db.connection.cursor()

            cursor.execute("SELECT name, instructor_id, email, department FROM instructors WHERE instructor_id = ?", (inst_id,))
            instructor = cursor.fetchone()

            if instructor:
                self.inst_name_var.set(instructor[0])
                self.inst_id_var.set(instructor[1])
                self.inst_email_var.set(instructor[2])
                self.inst_dept_var.set(instructor[3])

            db.close()

    def add_instructor(self):
        """Add Instructor and create login account."""
        name = self.inst_name_var.get().strip()
        inst_id = self.inst_id_var.get().strip()
        email = self.inst_email_var.get().strip()
        dept = self.inst_dept_var.get().strip()

        if name and inst_id:
            db = Database()
            db.connect()
            cursor = db.connection.cursor()

            try:
                # Insert into instructors table
                cursor.execute("INSERT INTO instructors (name, instructor_id, email, department) VALUES (?, ?, ?, ?)",
                               (name, inst_id, email, dept))

                # Insert into users table: username = Instructor Name
                hashed_password = Security.hash_password("12345").decode('utf-8')
                cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                               (name, hashed_password, "Instructor"))

                db.connection.commit()
                self.load_instructors()

                # Show Username + Default Password
                messagebox.showinfo("Success",
                                    f"Instructor and Login Account created successfully!\n\nUsername: {name}\nDefault Password: 12345")

            except Exception as e:
                messagebox.showerror("Error", f"Error adding instructor.\n{e}")

            db.close()
        else:
            messagebox.showwarning("Warning", "Please fill Name and ID.")

    def edit_instructor(self):
        """Edit Instructor."""
        name = self.inst_name_var.get()
        inst_id = self.inst_id_var.get()
        email = self.inst_email_var.get()
        dept = self.inst_dept_var.get()

        if name and inst_id:
            db = Database()
            db.connect()
            cursor = db.connection.cursor()

            try:
                cursor.execute("UPDATE instructors SET name=?, email=?, department=? WHERE instructor_id=?",
                               (name, email, dept, inst_id))
                db.connection.commit()
                self.load_instructors()
                messagebox.showinfo("Success", "Instructor updated successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Error updating instructor.\n{e}")

            db.close()
        else:
            messagebox.showwarning("Warning", "Please select an instructor.")

    def delete_instructor(self):
        """Delete Instructor."""
        inst_id = self.inst_id_var.get()

        if inst_id:
            if messagebox.askyesno("Confirm", "Are you sure to delete this instructor?"):
                db = Database()
                db.connect()
                cursor = db.connection.cursor()

                try:
                    cursor.execute("DELETE FROM instructors WHERE instructor_id=?", (inst_id,))
                    db.connection.commit()
                    self.load_instructors()
                    self.inst_name_var.set("")
                    self.inst_id_var.set("")
                    self.inst_email_var.set("")
                    self.inst_dept_var.set("")
                    messagebox.showinfo("Success", "Instructor deleted successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Error deleting instructor.\n{e}")

                db.close()

    # ---------------- Others ----------------

    def show_manage_students(self):
        """Manage Students Form and List."""
        self.clear_main_content()

        tk.Label(self.main_content, text="Manage Students 🎓", font=("Arial", 20, "bold"),
                 bg="#f0f0f0", fg="#2e2e2e").pack(pady=20)

        # After Title and before container:
        filter_frame = tk.Frame(self.main_content, bg="#f0f0f0")
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Select Class:", font=("Arial", 12),
                 bg="#f0f0f0", fg="#2e2e2e").pack(side="left", padx=5)

        self.class_filter_var = tk.StringVar()
        self.class_filter_combobox = ttk.Combobox(filter_frame, textvariable=self.class_filter_var, font=("Arial", 12),
                                                  width=20, state="readonly")
        self.class_filter_combobox.pack(side="left", padx=5)

        tk.Button(filter_frame, text="🔍 Filter", font=("Arial", 12),
                  bg="#dbe0e6", fg="#2e2e2e", command=self.filter_students_by_class).pack(side="left", padx=5)

        container = tk.Frame(self.main_content, bg="#f0f0f0")
        container.pack(expand=True, fill="both", padx=20)

        # Left Form Area
        form_frame = tk.Frame(container, bg="#f0f0f0")
        form_frame.pack(side="left", fill="y", padx=20)

        self.stud_name_var = tk.StringVar()
        self.stud_roll_var = tk.StringVar()
        self.stud_email_var = tk.StringVar()
        self.stud_class_var = tk.StringVar()

        fields = [("Student Name", self.stud_name_var),
                  ("Roll Number", self.stud_roll_var),
                  ("Email", self.stud_email_var),
                  ("Class", self.stud_class_var)]

        for label, var in fields:
            tk.Label(form_frame, text=label + ":", font=("Arial", 12), bg="#f0f0f0", fg="#2e2e2e").pack(pady=5,
                                                                                                        anchor="w")
            tk.Entry(form_frame, textvariable=var, font=("Arial", 12), width=25).pack(pady=5)

        # Buttons for Edit/Delete/View
        tk.Button(form_frame, text="✏️ Edit Student", width=20, font=("Arial", 12),
                  bg="#dbe0e6", fg="#2e2e2e", command=self.edit_student).pack(pady=10)
        tk.Button(form_frame, text="🗑️ Delete Student", width=20, font=("Arial", 12),
                  bg="#dbe0e6", fg="#2e2e2e", command=self.delete_student).pack(pady=10)
        tk.Button(form_frame, text="📋 View All Students", width=20, font=("Arial", 12),
                  bg="#dbe0e6", fg="#2e2e2e", command=self.view_all_students).pack(pady=10)

        # Right List Area
        list_frame = tk.Frame(container, bg="#f0f0f0")
        list_frame.pack(side="right", expand=True, fill="both")

        tk.Label(list_frame, text="Student List 📚", font=("Arial", 14, "bold"),
                 bg="#f0f0f0", fg="#2e2e2e").pack(pady=10)

        self.student_listbox = tk.Listbox(list_frame, font=("Arial", 12), bg="white", fg="#2e2e2e", height=20, width=50)
        self.student_listbox.pack(padx=10, pady=10, expand=True, fill="both")

        self.student_listbox.bind("<<ListboxSelect>>", self.load_student_to_form)

        self.load_students()

    def load_students(self, class_name=None):
        """Load all students into listbox. If class_name is provided, filter students."""
        self.student_listbox.delete(0, tk.END)
        db = Database()
        db.connect()
        cursor = db.connection.cursor()

        if class_name:
            cursor.execute("SELECT name, roll_number FROM students WHERE class_name=?", (class_name,))
        else:
            cursor.execute("SELECT name, roll_number FROM students")

        for row in cursor.fetchall():
            self.student_listbox.insert(tk.END, f"{row[0]} ({row[1]})")

        # Also update Class list for Combobox
        cursor.execute("SELECT DISTINCT class_name FROM students WHERE class_name IS NOT NULL")
        classes = [row[0] for row in cursor.fetchall()]
        self.class_filter_combobox["values"] = classes

        db.close()

    def load_student_to_form(self, event):
        """Load selected student to form fields."""
        selected = self.student_listbox.curselection()
        if selected:
            item = self.student_listbox.get(selected[0])
            name_part, roll_part = item.rsplit("(", 1)
            roll_number = roll_part.replace(")", "").strip()

            db = Database()
            db.connect()
            cursor = db.connection.cursor()

            cursor.execute("SELECT name, roll_number, email, class_name FROM students WHERE roll_number = ?",
                           (roll_number,))
            student = cursor.fetchone()

            if student:
                self.stud_name_var.set(student[0])
                self.stud_roll_var.set(student[1])
                self.stud_email_var.set(student[2])
                self.stud_class_var.set(student[3])

            db.close()

    def edit_student(self):
        """Edit selected student."""
        name = self.stud_name_var.get()
        roll = self.stud_roll_var.get()
        email = self.stud_email_var.get()
        class_name = self.stud_class_var.get()

        if name and roll:
            db = Database()
            db.connect()
            cursor = db.connection.cursor()

            try:
                cursor.execute("UPDATE students SET name=?, email=?, class_name=? WHERE roll_number=?",
                               (name, email, class_name, roll))
                db.connection.commit()
                self.load_students()
                messagebox.showinfo("Success", "Student updated successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Error updating student.\n{e}")

            db.close()
        else:
            messagebox.showwarning("Warning", "Please select a student.")

    def filter_students_by_class(self):
        """Filter students based on selected class."""
        selected_class = self.class_filter_var.get()
        if selected_class:
            self.load_students(class_name=selected_class)
        else:
            messagebox.showwarning("Warning", "Please select a class to filter.")

    def delete_student(self):
        """Delete selected student."""
        roll = self.stud_roll_var.get()

        if roll:
            if messagebox.askyesno("Confirm Delete", "Are you sure to delete this student?"):
                db = Database()
                db.connect()
                cursor = db.connection.cursor()

                try:
                    cursor.execute("DELETE FROM students WHERE roll_number=?", (roll,))
                    db.connection.commit()
                    self.load_students()
                    self.clear_student_form()
                    messagebox.showinfo("Success", "Student deleted successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Error deleting student.\n{e}")

                db.close()

    def clear_student_form(self):
        """Clear student form entries."""
        self.stud_name_var.set("")
        self.stud_roll_var.set("")
        self.stud_email_var.set("")
        self.stud_class_var.set("")

    def view_all_students(self):
        """View all students in table format inside main content."""
        self.clear_main_content()

        tk.Label(self.main_content, text="All Students 📋", font=("Arial", 20, "bold"),
                 bg="#f0f0f0", fg="#2e2e2e").pack(pady=20)

        table_frame = tk.Frame(self.main_content, bg="#f0f0f0")
        table_frame.pack(expand=True, fill="both", padx=20)

        headers = ["Roll Number", "Student Name", "Email", "Class Name"]
        for idx, header in enumerate(headers):
            tk.Label(table_frame, text=header, font=("Arial", 12, "bold"),
                     bg="#dbe0e6", fg="#2e2e2e", width=20, relief="groove").grid(row=0, column=idx, padx=1, pady=1)

        db = Database()
        db.connect()
        cursor = db.connection.cursor()

        cursor.execute("SELECT roll_number, name, email, class_name FROM students")
        students = cursor.fetchall()

        for row_idx, student in enumerate(students, start=1):
            for col_idx, value in enumerate(student):
                tk.Label(table_frame, text=value if value else "-", font=("Arial", 12),
                         bg="white", fg="#2e2e2e", width=20, relief="ridge").grid(row=row_idx, column=col_idx, padx=1,
                                                                                  pady=1)

        db.close()

        # Back Button
        tk.Button(self.main_content, text="🔙 Back to Manage Students", font=("Arial", 12, "bold"),
                  width=30, bg="#dbe0e6", fg="#2e2e2e", command=self.show_manage_students).pack(pady=20)

    def show_view_reports(self):
        """Show Attendance Reports View."""
        self.clear_main_content()

        tk.Label(self.main_content, text="Attendance Reports 📄", font=("Arial", 20, "bold"),
                 bg="#f0f0f0", fg="#2e2e2e").pack(pady=20)

        # Filter Area
        filter_frame = tk.Frame(self.main_content, bg="#f0f0f0")
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Select Class:", font=("Arial", 12), bg="#f0f0f0", fg="#2e2e2e").pack(side="left",
                                                                                                          padx=5)

        self.report_class_var = tk.StringVar()
        self.report_class_combobox = ttk.Combobox(filter_frame, textvariable=self.report_class_var, font=("Arial", 12),
                                                  width=20, state="readonly")
        self.report_class_combobox.pack(side="left", padx=5)

        tk.Button(filter_frame, text="🔍 Filter", font=("Arial", 12),
                  bg="#dbe0e6", fg="#2e2e2e", command=self.filter_reports_by_class).pack(side="left", padx=5)

        tk.Button(filter_frame, text="📄 View All Attendance", font=("Arial", 12),
                  bg="#dbe0e6", fg="#2e2e2e", command=self.load_all_attendance).pack(side="left", padx=5)

        # ➕ Export Button
        tk.Button(filter_frame, text="📥 Export CSV", font=("Arial", 12),
                  bg="#dbe0e6", fg="#2e2e2e", command=self.export_attendance_to_csv).pack(side="left", padx=5)

        # Table Area
        table_frame = tk.Frame(self.main_content, bg="#f0f0f0")
        table_frame.pack(expand=True, fill="both", padx=20, pady=10)

        columns = ("Date", "Student Name", "Roll Number", "Status")

        self.attendance_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.attendance_tree.heading(col, text=col)
            self.attendance_tree.column(col, anchor="center", width=200)

        self.attendance_tree.pack(expand=True, fill="both")

        self.load_class_list_for_reports()
        self.load_all_attendance()

    def export_attendance_to_csv(self):
        """Export current attendance table to CSV."""

        from tkinter import filedialog

        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv")],
                                                 title="Save Attendance Report")
        if not file_path:
            return  # User cancelled

        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                # Write header
                writer.writerow(["Date", "Student Name", "Roll Number", "Status"])

                # Write data
                for row_id in self.attendance_tree.get_children():
                    row = self.attendance_tree.item(row_id)['values']
                    writer.writerow(row)

            messagebox.showinfo("Success", f"Attendance report exported successfully!\nSaved at:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export CSV.\n{e}")

    def load_class_list_for_reports(self):
        """Load all classes into filter dropdown."""
        db = Database()
        db.connect()
        cursor = db.connection.cursor()

        cursor.execute("SELECT DISTINCT class_name FROM students WHERE class_name IS NOT NULL")
        classes = [row[0] for row in cursor.fetchall()]
        self.report_class_combobox["values"] = classes

        db.close()

    def load_all_attendance(self):
        """Load all attendance records."""
        self.attendance_tree.delete(*self.attendance_tree.get_children())

        db = Database()
        db.connect()
        cursor = db.connection.cursor()

        query = '''
            SELECT attendance.date, students.name, students.roll_number, attendance.status
            FROM attendance
            JOIN students ON attendance.student_id = students.id
            ORDER BY attendance.date DESC
        '''
        cursor.execute(query)
        records = cursor.fetchall()

        for record in records:
            self.attendance_tree.insert("", "end", values=record)

        db.close()

    def filter_reports_by_class(self):
        """Filter attendance records by selected class."""
        selected_class = self.report_class_var.get()

        if selected_class:
            self.attendance_tree.delete(*self.attendance_tree.get_children())

            db = Database()
            db.connect()
            cursor = db.connection.cursor()

            query = '''
                SELECT attendance.date, students.name, students.roll_number, attendance.status
                FROM attendance
                JOIN students ON attendance.student_id = students.id
                WHERE students.class_name = ?
                ORDER BY attendance.date DESC
            '''
            cursor.execute(query, (selected_class,))
            records = cursor.fetchall()

            for record in records:
                self.attendance_tree.insert("", "end", values=record)

            db.close()
        else:
            messagebox.showwarning("Warning", "Please select a class first.")

    def show_manage_class(self):
        """Manage Classes (Add/Edit/Delete/View/Assign)."""
        self.clear_main_content()

        tk.Label(self.main_content, text="Manage Classes 🏫", font=("Arial", 20, "bold"),
                 bg="#f0f0f0", fg="#2e2e2e").pack(pady=20)

        container = tk.Frame(self.main_content, bg="#f0f0f0")
        container.pack(expand=True, fill="both", padx=20)

        # Left Form
        form_frame = tk.Frame(container, bg="#f0f0f0")
        form_frame.pack(side="left", fill="y", padx=20)

        self.class_name_var = tk.StringVar()

        tk.Label(form_frame, text="Class Name:", font=("Arial", 12), bg="#f0f0f0", fg="#2e2e2e").pack(pady=5,
                                                                                                      anchor="w")
        tk.Entry(form_frame, textvariable=self.class_name_var, font=("Arial", 12), width=25).pack(pady=5)

        tk.Button(form_frame, text="➕ Add Class", width=20, font=("Arial", 12),
                  bg="#dbe0e6", fg="#2e2e2e", command=self.add_class).pack(pady=10)

        tk.Button(form_frame, text="✏️ Edit Class", width=20, font=("Arial", 12),
                  bg="#dbe0e6", fg="#2e2e2e", command=self.edit_class).pack(pady=10)

        tk.Button(form_frame, text="🗑️ Delete Class", width=20, font=("Arial", 12),
                  bg="#dbe0e6", fg="#2e2e2e", command=self.delete_class).pack(pady=10)

        tk.Button(form_frame, text="📋 View All Classes", width=20, font=("Arial", 12),
                  bg="#dbe0e6", fg="#2e2e2e", command=self.view_all_classes).pack(pady=10)

        tk.Button(form_frame, text="🔗 Assign Class to Instructor", width=20, font=("Arial", 12),
                  bg="#4d4d4d", fg="#ffffff", command=self.assign_class_to_instructor).pack(pady=20)

        # Right List Area
        list_frame = tk.Frame(container, bg="#f0f0f0")
        list_frame.pack(side="right", expand=True, fill="both")

        tk.Label(list_frame, text="Class List 📚", font=("Arial", 14, "bold"),
                 bg="#f0f0f0", fg="#2e2e2e").pack(pady=10)

        self.class_listbox = tk.Listbox(list_frame, font=("Arial", 12), bg="white", fg="#2e2e2e", height=20, width=40)
        self.class_listbox.pack(padx=10, pady=10, expand=True, fill="both")
        self.class_listbox.bind("<<ListboxSelect>>", self.load_class_to_form)

        self.load_classes()

    def load_classes(self):
        self.class_listbox.delete(0, tk.END)
        db = Database()
        db.connect()
        cursor = db.connection.cursor()
        cursor.execute("SELECT class_name FROM classes ORDER BY class_name ASC")
        for row in cursor.fetchall():
            self.class_listbox.insert(tk.END, row[0])
        db.close()

    def load_class_to_form(self, event):
        selected = self.class_listbox.curselection()
        if selected:
            class_name = self.class_listbox.get(selected[0])
            self.class_name_var.set(class_name)

    def add_class(self):
        class_name = self.class_name_var.get().strip()
        if class_name:
            db = Database()
            db.connect()
            cursor = db.connection.cursor()
            try:
                cursor.execute("INSERT INTO classes (class_name) VALUES (?)", (class_name,))
                db.connection.commit()
                self.load_classes()
                messagebox.showinfo("Success", "Class added successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Error adding class.\n{e}")
            db.close()
        else:
            messagebox.showwarning("Warning", "Please enter a class name.")

    def edit_class(self):
        selected = self.class_listbox.curselection()
        if selected:
            old_class_name = self.class_listbox.get(selected[0])
            new_class_name = self.class_name_var.get().strip()
            if new_class_name:
                db = Database()
                db.connect()
                cursor = db.connection.cursor()
                try:
                    cursor.execute("UPDATE classes SET class_name=? WHERE class_name=?",
                                   (new_class_name, old_class_name))
                    db.connection.commit()
                    self.load_classes()
                    messagebox.showinfo("Success", "Class name updated successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Error updating class.\n{e}")
                db.close()
            else:
                messagebox.showwarning("Warning", "Please enter a new class name.")

    def delete_class(self):
        """Delete selected class."""
        selected = self.class_listbox.curselection()
        if selected:
            class_name = self.class_listbox.get(selected[0])

            if messagebox.askyesno("Confirm Delete", "Are you sure to delete this class?"):
                db = Database()
                db.connect()
                cursor = db.connection.cursor()

                try:
                    cursor.execute("DELETE FROM classes WHERE class_name=?", (class_name,))
                    db.connection.commit()
                    self.load_classes()
                    self.class_name_var.set("")
                    messagebox.showinfo("Success", "Class deleted successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Error deleting class.\n{e}")

                db.close()

    def view_all_classes(self):
        """View all classes in table format."""
        self.clear_main_content()

        tk.Label(self.main_content, text="All Classes 📋", font=("Arial", 20, "bold"),
                 bg="#f0f0f0", fg="#2e2e2e").pack(pady=20)

        table_frame = tk.Frame(self.main_content, bg="#f0f0f0")
        table_frame.pack(expand=True, fill="both", padx=20)

        headers = ["Class Name"]
        for idx, header in enumerate(headers):
            tk.Label(table_frame, text=header, font=("Arial", 12, "bold"),
                     bg="#dbe0e6", fg="#2e2e2e", width=30, relief="groove").grid(row=0, column=idx, padx=1, pady=1)

        db = Database()
        db.connect()
        cursor = db.connection.cursor()

        cursor.execute("SELECT class_name FROM classes")
        classes = cursor.fetchall()

        for row_idx, class_row in enumerate(classes, start=1):
            tk.Label(table_frame, text=class_row[0], font=("Arial", 12),
                     bg="white", fg="#2e2e2e", width=30, relief="ridge").grid(row=row_idx, column=0, padx=1, pady=1)

        db.close()

        # Back Button
        tk.Button(self.main_content, text="🔙 Back to Manage Classes", font=("Arial", 12, "bold"),
                  width=30, bg="#dbe0e6", fg="#2e2e2e", command=self.show_manage_class).pack(pady=20)

    # Final Updated Assign Class using Dropdown of Instructors
    def assign_class_to_instructor(self):
        """Assign selected class to an instructor via Dropdown."""
        selected = self.class_listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a class first.")
            return

        selected_class_name = self.class_listbox.get(selected[0])

        # Create a Popup Window
        popup = tk.Toplevel(self.root)
        popup.title("Assign Class to Instructor")
        popup.geometry("400x200")
        popup.config(bg="#f0f0f0")

        tk.Label(popup, text=f"Assign '{selected_class_name}'", font=("Arial", 14, "bold"),
                 bg="#f0f0f0", fg="#2e2e2e").pack(pady=20)

        # Instructor Dropdown
        tk.Label(popup, text="Select Instructor:", font=("Arial", 12), bg="#f0f0f0", fg="#2e2e2e").pack()

        instructor_var = tk.StringVar()
        instructor_dropdown = ttk.Combobox(popup, textvariable=instructor_var, font=("Arial", 12), width=30,
                                           state="readonly")
        instructor_dropdown.pack(pady=10)

        # Load Instructors into Dropdown
        db = Database()
        db.connect()
        cursor = db.connection.cursor()
        cursor.execute("SELECT name FROM instructors")
        instructors = [row[0] for row in cursor.fetchall()]
        db.close()

        instructor_dropdown["values"] = instructors

        # Confirm Button
        def confirm_assignment():
            instructor_name = instructor_var.get()

            if instructor_name:
                db = Database()
                db.connect()
                cursor = db.connection.cursor()
                try:
                    cursor.execute("SELECT * FROM instructors WHERE name=?", (instructor_name,))
                    instructor = cursor.fetchone()

                    if instructor:
                        cursor.execute("UPDATE instructors SET department=? WHERE name=?",
                                       (selected_class_name, instructor_name))
                        db.connection.commit()
                        messagebox.showinfo("Success",
                                            f"Class '{selected_class_name}' assigned to '{instructor_name}'!")
                        popup.destroy()
                    else:
                        messagebox.showerror("Error", "Instructor not found.")

                except Exception as e:
                    messagebox.showerror("Error", f"Error assigning class.\n{e}")
                db.close()
            else:
                messagebox.showwarning("Warning", "Please select an Instructor.")

        tk.Button(popup, text="✅ Assign Class", font=("Arial", 12),
                  bg="#4d4d4d", fg="#ffffff", command=confirm_assignment).pack(pady=10)

    def show_admin_profile(self):
        """Admin Profile Settings (Update Username, Change Password)."""
        self.clear_main_content()

        tk.Label(self.main_content, text="Admin Profile ⚙️", font=("Arial", 20, "bold"),
                 bg="#f0f0f0", fg="#2e2e2e").pack(pady=20)

        profile_frame = tk.Frame(self.main_content, bg="#f0f0f0")
        profile_frame.pack(expand=True, fill="both", padx=20)

        # Username Section
        username_frame = tk.LabelFrame(profile_frame, text="Update Username", font=("Arial", 14, "bold"),
                                       bg="#dbe0e6", fg="#2e2e2e", padx=20, pady=20, labelanchor="n")
        username_frame.pack(fill="x", pady=20)

        tk.Label(username_frame, text="Current Username:", font=("Arial", 12), bg="#dbe0e6", fg="#2e2e2e").grid(row=0,
                                                                                                                column=0,
                                                                                                                pady=5,
                                                                                                                sticky="w")
        tk.Label(username_frame, text=self.username, font=("Arial", 12, "bold"), bg="#dbe0e6", fg="#2e2e2e").grid(row=0,
                                                                                                                  column=1,
                                                                                                                  pady=5,
                                                                                                                  sticky="w")

        tk.Label(username_frame, text="New Username:", font=("Arial", 12), bg="#dbe0e6", fg="#2e2e2e").grid(row=1,
                                                                                                            column=0,
                                                                                                            pady=5,
                                                                                                            sticky="w")
        self.new_username_var = tk.StringVar()
        tk.Entry(username_frame, textvariable=self.new_username_var, font=("Arial", 12), width=25).grid(row=1, column=1,
                                                                                                        pady=5)

        tk.Button(username_frame, text="✏️ Update Username", font=("Arial", 12),
                  bg="#4d4d4d", fg="white", command=self.update_username).grid(row=2, columnspan=2, pady=10)

        # Password Section
        password_frame = tk.LabelFrame(profile_frame, text="Change Password", font=("Arial", 14, "bold"),
                                       bg="#dbe0e6", fg="#2e2e2e", padx=20, pady=20, labelanchor="n")
        password_frame.pack(fill="x", pady=20)

        tk.Label(password_frame, text="Old Password:", font=("Arial", 12), bg="#dbe0e6", fg="#2e2e2e").grid(row=0,
                                                                                                            column=0,
                                                                                                            pady=5,
                                                                                                            sticky="w")
        self.old_pass_var = tk.StringVar()
        tk.Entry(password_frame, textvariable=self.old_pass_var, show="*", font=("Arial", 12), width=25).grid(row=0,
                                                                                                              column=1,
                                                                                                              pady=5)

        tk.Label(password_frame, text="New Password:", font=("Arial", 12), bg="#dbe0e6", fg="#2e2e2e").grid(row=1,
                                                                                                            column=0,
                                                                                                            pady=5,
                                                                                                            sticky="w")
        self.new_pass_var = tk.StringVar()
        tk.Entry(password_frame, textvariable=self.new_pass_var, show="*", font=("Arial", 12), width=25).grid(row=1,
                                                                                                              column=1,
                                                                                                              pady=5)

        tk.Label(password_frame, text="Confirm Password:", font=("Arial", 12), bg="#dbe0e6", fg="#2e2e2e").grid(row=2,
                                                                                                                column=0,
                                                                                                                pady=5,
                                                                                                                sticky="w")
        self.confirm_pass_var = tk.StringVar()
        tk.Entry(password_frame, textvariable=self.confirm_pass_var, show="*", font=("Arial", 12), width=25).grid(row=2,
                                                                                                                  column=1,
                                                                                                                  pady=5)

        tk.Button(password_frame, text="🔒 Change Password", font=("Arial", 12),
                  bg="#4d4d4d", fg="white", command=self.change_password).grid(row=3, columnspan=2, pady=10)

    def update_username(self):
        """Update admin's username."""
        new_username = self.new_username_var.get().strip()

        if new_username:
            db = Database()
            db.connect()
            cursor = db.connection.cursor()

            try:
                cursor.execute("UPDATE users SET username=? WHERE username=?", (new_username, self.username))
                db.connection.commit()
                self.username = new_username  # Update session username
                messagebox.showinfo("Success", "Username updated successfully!")
                self.show_admin_profile()  # Reload screen
            except Exception as e:
                messagebox.showerror("Error", f"Error updating username.\n{e}")

            db.close()
        else:
            messagebox.showwarning("Warning", "Please enter a new username.")

    from StudentAttendanceTracker.utils.security import Security  # Assuming you have password hashing module
    def change_password(self):
        """Change admin's password."""
        old_pass = self.old_pass_var.get().strip()
        new_pass = self.new_pass_var.get().strip()
        confirm_pass = self.confirm_pass_var.get().strip()

        if old_pass and new_pass and confirm_pass:
            db = Database()
            db.connect()
            cursor = db.connection.cursor()

            cursor.execute("SELECT password FROM users WHERE username=?", (self.username,))
            record = cursor.fetchone()

            if record:
                stored_password = record[0]
                if Security.verify_password(old_pass, stored_password):
                    if new_pass == confirm_pass:
                        hashed_password = Security.hash_password(new_pass).decode('utf-8')
                        cursor.execute("UPDATE users SET password=? WHERE username=?", (hashed_password, self.username))
                        db.connection.commit()
                        messagebox.showinfo("Success", "Password changed successfully!")
                        self.old_pass_var.set("")
                        self.new_pass_var.set("")
                        self.confirm_pass_var.set("")
                    else:
                        messagebox.showwarning("Warning", "New passwords do not match.")
                else:
                    messagebox.showerror("Error", "Old password is incorrect.")
            else:
                messagebox.showerror("Error", "User record not found.")

            db.close()
        else:
            messagebox.showwarning("Warning", "Please fill all password fields.")


    def toggle_theme(self):
        """Toggle Dark/Light Theme."""
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme()

    def apply_theme(self):
        """Apply theme to GUI."""
        if self.is_dark_mode:
            sidebar_bg = "#2e2e2e"
            main_bg = "#3d3d3d"
            fg_color = "#ffffff"
            button_bg = "#4d4d4d"
        else:
            sidebar_bg = "#dbe0e6"
            main_bg = "#f0f0f0"
            fg_color = "#2e2e2e"
            button_bg = "#dbe0e6"

        self.sidebar.config(bg=sidebar_bg)
        self.main_content.config(bg=main_bg)

        for widget in self.sidebar.winfo_children():
            if isinstance(widget, tk.Button):
                if "Logout" in widget["text"]:
                    widget.config(bg="red", fg="white")
                elif "Theme" in widget["text"]:
                    widget.config(bg="#4d4d4d", fg="white")
                else:
                    widget.config(bg=button_bg, fg=fg_color)

    def logout(self):
        """Logout and return to login screen."""
        if messagebox.askyesno("Confirm Logout", "Are you sure you want to logout?"):
            self.root.destroy()

            import tkinter as tk
            from StudentAttendanceTracker.view.login_window import LoginWindow  # Import your LoginWindow

            new_root = tk.Tk()
            LoginWindow(new_root)
            new_root.mainloop()

