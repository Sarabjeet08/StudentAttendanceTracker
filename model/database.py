# model/database.py
# OOP Concept: Class, Object, Encapsulation, Database Management

import sqlite3

class Database:
    """Handles database connection and queries."""

    def __init__(self, db_name="attendance.db"):
        """Initialize with database name."""
        self.db_name = db_name
        self.connection = None

    def connect(self):
        """Connect to the SQLite database."""
        try:
            self.connection = sqlite3.connect(self.db_name)
            print("✅ Database connection successful.")
        except sqlite3.Error as e:
            print(f"❌ Database connection failed: {e}")

    def create_tables(self):
        """Create all necessary tables."""
        try:
            cursor = self.connection.cursor()

            # Students Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    roll_number TEXT UNIQUE NOT NULL,
                    email TEXT,
                    class_name TEXT,
                    photo BLOB,
                    instructor_username TEXT
                )
            ''')

            # Users Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL
                )
            ''')

            # Attendance Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    date TEXT NOT NULL,
                    status TEXT NOT NULL,
                    FOREIGN KEY(student_id) REFERENCES students(id)
                )
            ''')

            # Instructors Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS instructors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    instructor_id TEXT UNIQUE NOT NULL,
                    email TEXT,
                    department TEXT
                )
            ''')

            # Classes Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS classes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    class_name TEXT UNIQUE NOT NULL
                )
            ''')

            self.connection.commit()
            print("✅ All tables created successfully.")
        except sqlite3.Error as e:
            print(f"❌ Error creating tables: {e}")

    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            print("✅ Database connection closed.")

