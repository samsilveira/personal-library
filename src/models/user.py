"""
Module containing the User class.
"""

from .collection import Collection
from .configuration import Configuration

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
        self.configuration = Configuration()
        self.configuration.load_settings()
        self.collection = Collection()

    def __str__(self):
        """Returns a string representation of the publication."""
        return f"User: {self.name} ({self.email})"
    
    def start_reading(self, publication_id: int) -> bool:
        """
        Start reading a publication with automatic validation.

        Args:
            publication_id: ID of the publication to start

        Returns:
            True if started successfully

        Raises:
            ValueErros: If simultaneous reading limit is reached
        """
        return self.collection.start_publication_reading(
            publication_id,
            self.configuration
        )
