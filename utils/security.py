# utils/security.py
# OOP Concept: Encapsulation (hiding password logic inside methods)

import bcrypt

class Security:
    """Handles password hashing and verification."""

    @staticmethod
    def hash_password(password):
        """Hash a password."""
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    @staticmethod
    def verify_password(password, hashed_password):
        """Verify a password against a hashed password."""
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode()  # Convert str to bytes
        return bcrypt.checkpw(password.encode(), hashed_password)
