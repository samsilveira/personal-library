"""
Module containing the User class.
"""

class User:
    """
    Represents the library owner.

    Simple class for personalization purposes, storing basic user information.

    Attributes:
        name (str): User's name
        email (str): User's email address
    """

    def __init__(self, name: str, email: str):
        """
        Initialize a new user.

        Args:
            name: User's name
            email: User's email address
        """
        if not name or not name.strip():
            raise ValueError("Name cannot be empty")
        self.name = name.strip()
        self.email = email

    def __str__(self):
        """Returns a string representation of the publication."""
        return f"User: {self.name} ({self.email})"