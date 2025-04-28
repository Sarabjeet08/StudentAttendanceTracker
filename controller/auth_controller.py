# controller/auth_controller.py
# OOP Concept: Class, Encapsulation, Composition (Database and Security classes)

from StudentAttendanceTracker.model.database import Database
from StudentAttendanceTracker.utils.security import Security


class AuthController:
    """Handles user authentication by connecting to the database and verifying credentials."""

    def __init__(self):
        """Initialize the database connection."""
        self.db = Database()
        self.db.connect()

    def login(self, username, password):
        """Authenticate user with username and password.

        Args:
            username (str): Entered username.
            password (str): Entered password.

        Returns:
            str or None: Returns user's role if authentication is successful, otherwise None.
        """
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT password, role FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user:
            stored_hashed_password, role = user
            stored_hashed_password = stored_hashed_password.encode('utf-8')  # Fix: encode to bytes
            if Security.verify_password(password, stored_hashed_password):
                return role
            else:
                return None  # Password incorrect
        else:
            return None  # Username not found

    def __del__(self):
        """Ensure the database connection is closed when object is deleted."""
        self.db.close()
