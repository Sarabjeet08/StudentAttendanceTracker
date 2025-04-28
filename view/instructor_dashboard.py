# view/instructor_dashboard.py
# OOP Concept: Class, Encapsulation, Instructor Specific Dashboard

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from StudentAttendanceTracker.model.database import Database
from StudentAttendanceTracker.utils.security import Security

class InstructorDashboard:
    """Instructor Dashboard - Manage Students, Attendance, Reports."""

    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title("Instructor Dashboard - Student Attendance Tracker")
        self.root.geometry("1150x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#2e2e2e")

        self.create_top_bar()
        self.sidebar = tk.Frame(self.root, width=270, bg="#2e2e2e")
        self.sidebar.pack(side="left", fill="y")
        self.main_content = tk.Frame(self.root, bg="#f0f0f0")
        self.main_content.pack(expand=True, fill="both")

        self.add_sidebar_buttons()
        self.is_dark_mode = False
        self.apply_theme()
        self.show_dashboard_overview()

    def create_top_bar(self):
        bar = tk.Frame(self.root, height=40, bg="#dbe0e6")
        bar.pack(side="top", fill="x")
        tk.Label(bar, text=f"Welcome, {self.username} 👩‍🏫", font=("Arial", 14, "bold"),
                 bg="#dbe0e6", fg="#2e2e2e", anchor="w", padx=20).pack(fill="both")

    def add_sidebar_buttons(self):
        settings = {"font": ("Arial", 12, "bold"), "width": 22, "height": 2, "bg": "#dbe0e6", "fg": "#2e2e2e", "bd": 0}

        buttons = [
            ("🎯 Dashboard", self.show_dashboard_overview),
            ("🎓 Manage Students", self.show_manage_students),
            ("📝 Mark Attendance", self.show_mark_attendance),
            ("📄 View Reports", self.show_view_reports),
            ("⚙️ Profile", self.show_profile)
        ]

        for text, command in buttons:
            tk.Button(self.sidebar, text=text, command=command, **settings).pack(pady=10, padx=10)

        tk.Button(self.sidebar, text="🔒 Logout", command=self.logout,
                  font=("Arial", 12, "bold"), width=22, height=2, bg="red", fg="white", bd=0).pack(pady=20, padx=10)

    def clear_main_content(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def show_dashboard_overview(self):
        """Show Instructor Dashboard Overview with Stats."""
        self.clear_main_content()

        tk.Label(self.main_content, text=f"Welcome, {self.username} 👩‍🏫", font=("Arial", 22, "bold"),
                 bg="#f0f0f0", fg="#2e2e2e").pack(pady=30)

        stats_frame = tk.Frame(self.main_content, bg="#f0f0f0")
        stats_frame.pack(pady=10, padx=20)

        # Fetch stats
        total_students = self.get_total_students()
        total_attendance = self.get_total_attendance()
        total_classes = self.get_total_classes()

        cards = [
            ("🎓 Total Students", total_students),
            ("📄 Attendance Records", total_attendance),
            ("🏫 Classes Handled", total_classes)
        ]

        for idx, (label, count) in enumerate(cards):
            card = tk.Frame(stats_frame, bg="#dbe0e6", width=250, height=150, bd=2, relief="ridge")
            card.grid(row=0, column=idx, padx=20, pady=20)
            tk.Label(card, text=label, font=("Arial", 12, "bold"), bg="#dbe0e6", fg="#2e2e2e").pack(pady=10)
            tk.Label(card, text=str(count), font=("Arial", 24, "bold"), bg="#dbe0e6", fg="#2e2e2e").pack()

    def get_total_students(self):
        """Get total students created by Instructor."""
        db = Database()
        db.connect()
        cursor = db.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM students WHERE instructor_username=?", (self.username,))
        count = cursor.fetchone()[0]
        db.close()
        return count

    def get_total_attendance(self):
        """Get total attendance records for Instructor's students."""
        db = Database()
        db.connect()
        cursor = db.connection.cursor()
        query = '''
            SELECT COUNT(*)
            FROM attendance
            WHERE student_id IN (
                SELECT id FROM students WHERE instructor_username=?
            )
        '''
        cursor.execute(query, (self.username,))
        count = cursor.fetchone()[0]
        db.close()
        return count

    def get_total_classes(self):
        """Get total distinct classes Instructor is handling."""
        db = Database()
        db.connect()
        cursor = db.connection.cursor()
        cursor.execute("SELECT COUNT(DISTINCT class_name) FROM students WHERE instructor_username=?", (self.username,))
        count = cursor.fetchone()[0]
        db.close()
        return count

    def show_manage_students(self):
        """Show Manage Students Page."""
        self.clear_main_content()
        tk.Label(self.main_content, text="Manage Your Students 🎓", font=("Arial", 20, "bold"),
                 bg="#f0f0f0", fg="#2e2e2e").pack(pady=20)

        form_frame = tk.Frame(self.main_content, bg="#f0f0f0")
        form_frame.pack(pady=10)

        self.stud_name_var = tk.StringVar()
        self.stud_roll_var = tk.StringVar()
        self.stud_email_var = tk.StringVar()
        self.stud_class_var = tk.StringVar()

        fields = [("Name", self.stud_name_var), ("Roll No.", self.stud_roll_var),
                  ("Email", self.stud_email_var), ("Class", self.stud_class_var)]

        for idx, (label, var) in enumerate(fields):
            tk.Label(form_frame, text=label, font=("Arial", 12), bg="#f0f0f0", fg="#2e2e2e").grid(row=idx, column=0,
                                                                                                  sticky="w", pady=5)
            if label == "Class":
                self.class_combobox = ttk.Combobox(form_frame, textvariable=var, font=("Arial", 12), width=27,
                                                   state="readonly")
                self.class_combobox.grid(row=idx, column=1, pady=5)
                self.load_classes_for_dropdown()
            else:
                tk.Entry(form_frame, textvariable=var, font=("Arial", 12), width=30).grid(row=idx, column=1, pady=5)

        # Buttons
        tk.Button(form_frame, text="➕ Add Student", font=("Arial", 12), command=self.add_student).grid(row=5, column=0,
                                                                                                       pady=10)
        tk.Button(form_frame, text="✏️ Edit Student", font=("Arial", 12), command=self.edit_student).grid(row=5,
                                                                                                          column=1,
                                                                                                          pady=10)
        tk.Button(form_frame, text="🗑️ Delete Student", font=("Arial", 12), command=self.delete_student).grid(row=5,
                                                                                                              column=2,
                                                                                                              pady=10)

        # Listbox for Students
        self.students_listbox = tk.Listbox(self.main_content, font=("Arial", 12), width=100)
        self.students_listbox.pack(pady=20)
        self.students_listbox.bind("<<ListboxSelect>>", self.load_selected_student)

        self.load_students()

    def load_classes_for_dropdown(self):
        """Load all available Classes into Combobox."""
        db = Database()
        db.connect()
        cursor = db.connection.cursor()
        cursor.execute("SELECT class_name FROM classes ORDER BY class_name ASC")
        classes = [row[0] for row in cursor.fetchall()]
        self.class_combobox["values"] = classes
        db.close()

    def load_students(self):
        """Load Instructor's Students into Listbox."""
        self.students_listbox.delete(0, tk.END)
        db = Database()
        db.connect()
        cursor = db.connection.cursor()
        cursor.execute("SELECT name, roll_number FROM students WHERE instructor_username=?", (self.username,))
        students = cursor.fetchall()
        for student in students:
            self.students_listbox.insert(tk.END, f"{student[0]} ({student[1]})")
        db.close()

    def load_selected_student(self, event):
        """Load selected student data into form."""
        selection = self.students_listbox.curselection()
        if selection:
            value = self.students_listbox.get(selection[0])
            name, roll = value.rsplit("(", 1)
            self.stud_name_var.set(name.strip())
            self.stud_roll_var.set(roll.replace(")", "").strip())
            # Optional: You can also load email and class if you want here

    def add_student(self):
        """Add a New Student."""
        name = self.stud_name_var.get().strip()
        roll = self.stud_roll_var.get().strip()
        email = self.stud_email_var.get().strip()
        class_name = self.stud_class_var.get().strip()

        if name and roll and class_name:
            db = Database()
            db.connect()
            cursor = db.connection.cursor()
            cursor.execute(
                "INSERT INTO students (name, roll_number, email, class_name, instructor_username) VALUES (?, ?, ?, ?, ?)",
                (name, roll, email, class_name, self.username))
            db.connection.commit()
            db.close()
            self.load_students()
            messagebox.showinfo("Success", "Student Added Successfully!")
        else:
            messagebox.showwarning("Warning", "Please fill all fields.")

    def edit_student(self):
        """Edit Selected Student."""
        name = self.stud_name_var.get().strip()
        roll = self.stud_roll_var.get().strip()
        email = self.stud_email_var.get().strip()
        class_name = self.stud_class_var.get().strip()

        db = Database()
        db.connect()
        cursor = db.connection.cursor()
        cursor.execute(
            "UPDATE students SET name=?, email=?, class_name=? WHERE roll_number=? AND instructor_username=?",
            (name, email, class_name, roll, self.username))
        db.connection.commit()
        db.close()
        self.load_students()
        messagebox.showinfo("Success", "Student Updated Successfully!")

    def delete_student(self):
        """Delete Selected Student."""
        roll = self.stud_roll_var.get().strip()

        db = Database()
        db.connect()
        cursor = db.connection.cursor()
        cursor.execute("DELETE FROM students WHERE roll_number=? AND instructor_username=?", (roll, self.username))
        db.connection.commit()
        db.close()
        self.load_students()
        messagebox.showinfo("Success", "Student Deleted Successfully!")

    def show_mark_attendance(self):
        """Show Mark Attendance Page by Class and Students List."""
        self.clear_main_content()
        tk.Label(self.main_content, text="Mark Attendance 📝", font=("Arial", 20, "bold"),
                 bg="#f0f0f0", fg="#2e2e2e").pack(pady=20)

        top_frame = tk.Frame(self.main_content, bg="#f0f0f0")
        top_frame.pack(pady=10)

        # Class Dropdown
        tk.Label(top_frame, text="Select Class:", font=("Arial", 12), bg="#f0f0f0", fg="#2e2e2e").grid(row=0, column=0,
                                                                                                       padx=5)
        self.selected_class_var = tk.StringVar()
        self.class_combobox = ttk.Combobox(top_frame, textvariable=self.selected_class_var, font=("Arial", 12),
                                           width=30, state="readonly")
        self.class_combobox.grid(row=0, column=1, padx=5)
        self.load_classes_for_attendance()

        tk.Button(top_frame, text="🔍 Load Students", font=("Arial", 12),
                  command=self.load_students_for_selected_class).grid(row=0, column=2, padx=10)

        # Students Table Area
        self.student_attendance_frame = tk.Frame(self.main_content, bg="#f0f0f0")
        self.student_attendance_frame.pack(pady=20, expand=True, fill="both")

        self.student_widgets = []  # to store (student_id, attendance_status_var)

        tk.Button(self.main_content, text="✅ Save Attendance", font=("Arial", 14),
                  command=self.save_all_attendance).pack(pady=20)

    def load_classes_for_attendance(self):
        """Load available classes into Class Combobox."""
        db = Database()
        db.connect()
        cursor = db.connection.cursor()
        cursor.execute("SELECT DISTINCT class_name FROM students WHERE instructor_username=?", (self.username,))
        classes = [row[0] for row in cursor.fetchall()]
        self.class_combobox["values"] = classes
        db.close()

    def load_students_for_selected_class(self):
        """Load Students of Selected Class."""
        # Clear previous
        for widget in self.student_attendance_frame.winfo_children():
            widget.destroy()

        selected_class = self.selected_class_var.get()
        if not selected_class:
            messagebox.showwarning("Warning", "Please select a class first.")
            return

        db = Database()
        db.connect()
        cursor = db.connection.cursor()
        cursor.execute("SELECT id, name, roll_number FROM students WHERE class_name=? AND instructor_username=?",
                       (selected_class, self.username))
        students = cursor.fetchall()
        db.close()

        self.student_widgets = []

        # Table Headers
        headers = ["Roll Number", "Student Name", "Attendance Status"]
        for idx, header in enumerate(headers):
            tk.Label(self.student_attendance_frame, text=header, font=("Arial", 12, "bold"),
                     bg="#dbe0e6", fg="#2e2e2e", width=20, relief="ridge").grid(row=0, column=idx, padx=1, pady=1)

        # Student Rows
        for row_idx, (student_id, name, roll_no) in enumerate(students, start=1):
            tk.Label(self.student_attendance_frame, text=roll_no, font=("Arial", 12),
                     bg="white", fg="#2e2e2e", width=20, relief="ridge").grid(row=row_idx, column=0, padx=1, pady=1)

            tk.Label(self.student_attendance_frame, text=name, font=("Arial", 12),
                     bg="white", fg="#2e2e2e", width=20, relief="ridge").grid(row=row_idx, column=1, padx=1, pady=1)

            attendance_var = tk.StringVar(value="Present")
            status_combobox = ttk.Combobox(self.student_attendance_frame, textvariable=attendance_var,
                                           font=("Arial", 12), width=18, state="readonly")
            status_combobox["values"] = ["Present", "Absent"]
            status_combobox.grid(row=row_idx, column=2, padx=1, pady=1)

            self.student_widgets.append((student_id, attendance_var))

    def save_all_attendance(self):
        """Save Attendance for All Students."""
        if not self.student_widgets:
            messagebox.showwarning("Warning", "No students to save attendance for.")
            return

        import datetime
        today_date = datetime.date.today().strftime("%Y-%m-%d")

        db = Database()
        db.connect()
        cursor = db.connection.cursor()

        for student_id, attendance_var in self.student_widgets:
            status = attendance_var.get()
            cursor.execute("INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)",
                           (student_id, today_date, status))

        db.connection.commit()
        db.close()

        messagebox.showinfo("Success", "Attendance Saved Successfully!")
        self.show_mark_attendance()  # reload fresh

    def mark_attendance_now(self):
        """Save Attendance Record into Database."""
        selected_student = self.attendance_student_var.get()
        status = self.attendance_status_var.get()

        if not selected_student or not status:
            messagebox.showwarning("Warning", "Please select both Student and Attendance Status.")
            return

        # Extract Roll Number
        name_part, roll_part = selected_student.rsplit("(", 1)
        roll_number = roll_part.replace(")", "").strip()

        db = Database()
        db.connect()
        cursor = db.connection.cursor()

        # Get student_id based on roll_number
        cursor.execute("SELECT id FROM students WHERE roll_number=? AND instructor_username=?",
                       (roll_number, self.username))
        result = cursor.fetchone()

        if result:
            student_id = result[0]

            import datetime
            today_date = datetime.date.today().strftime("%Y-%m-%d")

            # Insert Attendance
            cursor.execute("INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)",
                           (student_id, today_date, status))
            db.connection.commit()
            messagebox.showinfo("Success", "Attendance marked successfully!")
        else:
            messagebox.showerror("Error", "Student not found!")

        db.close()

        # Refresh Students if needed
        self.load_students_for_attendance()

    # Full Updated show_view_reports with Class and Date Range Filters
    def show_view_reports(self):
        """Show Attendance Reports with Class and Date Filters."""
        self.clear_main_content()
        tk.Label(self.main_content, text="Attendance Reports 📄", font=("Arial", 20, "bold"),
                 bg="#f0f0f0", fg="#2e2e2e").pack(pady=20)

        filter_frame = tk.Frame(self.main_content, bg="#f0f0f0")
        filter_frame.pack(pady=10)

        # Class Dropdown
        tk.Label(filter_frame, text="Select Class:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, padx=5)
        self.filter_class_var = tk.StringVar()
        self.class_combobox = ttk.Combobox(filter_frame, textvariable=self.filter_class_var, font=("Arial", 12),
                                           width=20, state="readonly")
        self.class_combobox.grid(row=0, column=1, padx=5)
        self.load_classes_for_reports()

        # Start Date
        tk.Label(filter_frame, text="Start Date (YYYY-MM-DD):", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=2,
                                                                                                       padx=5)
        self.start_date_var = tk.StringVar()
        tk.Entry(filter_frame, textvariable=self.start_date_var, font=("Arial", 12), width=20).grid(row=0, column=3,
                                                                                                    padx=5)

        # End Date
        tk.Label(filter_frame, text="End Date (YYYY-MM-DD):", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=2,
                                                                                                     padx=5)
        self.end_date_var = tk.StringVar()
        tk.Entry(filter_frame, textvariable=self.end_date_var, font=("Arial", 12), width=20).grid(row=1, column=3,
                                                                                                  padx=5)

        # Buttons
        tk.Button(filter_frame, text="🔍 Filter", font=("Arial", 12), command=self.filter_attendance_reports).grid(row=0,
                                                                                                                  column=6,
                                                                                                                  padx=10)
        tk.Button(filter_frame, text="📄 View All Attendance", font=("Arial", 12),
                  command=self.load_all_attendance).grid(row=1, column=6, padx=10)

        # Table Area
        table_frame = tk.Frame(self.main_content, bg="#f0f0f0")
        table_frame.pack(pady=20, expand=True, fill="both")

        columns = ("Date", "Student Name", "Roll No", "Status")
        self.attendance_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.attendance_tree.heading(col, text=col)
            self.attendance_tree.column(col, anchor="center", width=150)

        self.attendance_tree.pack(expand=True, fill="both")

        self.load_all_attendance()

    def load_classes_for_reports(self):
        """Load Classes into filter dropdown."""
        db = Database()
        db.connect()
        cursor = db.connection.cursor()
        cursor.execute("SELECT DISTINCT class_name FROM students WHERE instructor_username=?", (self.username,))
        classes = [row[0] for row in cursor.fetchall()]
        self.class_combobox["values"] = classes
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
            WHERE students.instructor_username=?
            ORDER BY attendance.date DESC
        '''
        cursor.execute(query, (self.username,))
        records = cursor.fetchall()

        for record in records:
            self.attendance_tree.insert("", "end", values=record)

        db.close()

    def filter_attendance_reports(self):
        """Filter attendance records based on selected filters."""
        self.attendance_tree.delete(*self.attendance_tree.get_children())

        selected_class = self.filter_class_var.get()
        start_date = self.start_date_var.get()
        end_date = self.end_date_var.get()

        query = '''
            SELECT attendance.date, students.name, students.roll_number, attendance.status
            FROM attendance
            JOIN students ON attendance.student_id = students.id
            WHERE students.instructor_username=?
        '''
        params = [self.username]

        if selected_class:
            query += " AND students.class_name=?"
            params.append(selected_class)

        if start_date and end_date:
            query += " AND attendance.date BETWEEN ? AND ?"
            params.extend([start_date, end_date])

        query += " ORDER BY attendance.date DESC"

        db = Database()
        db.connect()
        cursor = db.connection.cursor()
        cursor.execute(query, tuple(params))
        records = cursor.fetchall()

        for record in records:
            self.attendance_tree.insert("", "end", values=record)

        db.close()

    def show_profile(self):
        """Show Profile Settings to Change Password."""
        self.clear_main_content()
        tk.Label(self.main_content, text="Profile Settings ⚙️", font=("Arial", 20, "bold"),
                 bg="#f0f0f0", fg="#2e2e2e").pack(pady=20)

        profile_frame = tk.Frame(self.main_content, bg="#f0f0f0")
        profile_frame.pack(pady=10)

        self.old_pass_var = tk.StringVar()
        self.new_pass_var = tk.StringVar()
        self.confirm_pass_var = tk.StringVar()

        fields = [("Old Password", self.old_pass_var), ("New Password", self.new_pass_var),
                  ("Confirm Password", self.confirm_pass_var)]

        for idx, (label, var) in enumerate(fields):
            tk.Label(profile_frame, text=label + ":", font=("Arial", 12), bg="#f0f0f0", fg="#2e2e2e").grid(row=idx,
                                                                                                           column=0,
                                                                                                           sticky="w",
                                                                                                           pady=5)
            tk.Entry(profile_frame, textvariable=var, font=("Arial", 12), width=30, show="*").grid(row=idx, column=1,
                                                                                                   pady=5)

        tk.Button(profile_frame, text="🔒 Change Password", font=("Arial", 12),
                  command=self.change_instructor_password).grid(row=4, columnspan=2, pady=20)

    def change_instructor_password(self):
        """Change Instructor Password."""
        old_pass = self.old_pass_var.get().strip()
        new_pass = self.new_pass_var.get().strip()
        confirm_pass = self.confirm_pass_var.get().strip()

        if not old_pass or not new_pass or not confirm_pass:
            messagebox.showwarning("Warning", "Please fill all fields.")
            return

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
            messagebox.showerror("Error", "User not found!")

        db.close()

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme()

    def apply_theme(self):
        if self.is_dark_mode:
            sidebar_bg, main_bg, fg_color, button_bg = "#2e2e2e", "#3d3d3d", "#ffffff", "#4d4d4d"
        else:
            sidebar_bg, main_bg, fg_color, button_bg = "#dbe0e6", "#f0f0f0", "#2e2e2e", "#dbe0e6"

        self.sidebar.config(bg=sidebar_bg)
        self.main_content.config(bg=main_bg)

        for widget in self.sidebar.winfo_children():
            if isinstance(widget, tk.Button):
                if "Logout" in widget["text"]:
                    widget.config(bg="red", fg="white")
                else:
                    widget.config(bg=button_bg, fg=fg_color)

    def logout(self):
        if messagebox.askyesno("Confirm Logout", "Are you sure you want to logout?"):
            self.root.destroy()

            import tkinter as tk
            from StudentAttendanceTracker.view.login_window import LoginWindow
            new_root = tk.Tk()
            LoginWindow(new_root)
            new_root.mainloop()
