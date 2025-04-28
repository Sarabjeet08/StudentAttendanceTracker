# main.py
# OOP Concept: Object Initialization, Class Usage

import tkinter as tk
from StudentAttendanceTracker.view.login_window import LoginWindow
from StudentAttendanceTracker.model.database import Database

def main():
    # Initialize database and create tables
    db = Database()
    db.connect()
    db.create_tables()
    db.close()

    # Launch login window
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
