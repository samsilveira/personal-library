"""
Module containing the User class.
"""

import re
from typing import Optional
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

    def __init__(
        self,
        name: str,
        email: str,
        collection: Optional[Collection] = None,
        configuration: Optional[Configuration] = None
    ):
        """
        Initialize a new user.

        Args:
            name: User's name
            email: User's email address
            collection: Optional custom collection (creates new if None)
            configuration: Optional custom configuration (creates new if None)
        """
        if not name or not name.strip():
            raise ValueError("Name cannot be empty")
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format")
        
        self.name = name.strip()
        self.email = email
        
        if configuration is None:
            self.configuration = Configuration()
            self.configuration.load_settings()
        else:
            self.configuration = configuration
        
        if collection is None:
            self.collection = Collection()
        else:
            self.collection = collection

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
    
    def to_dict(self) -> dict:
        """
        Serialize user to dictionary.
        
        Returns:
            Dictionary with user data including collection and configuration
        """
        return {
            'name': self.name,
            'email': self.email,
            'collection': self.collection.to_dict(),
            'configuration': self.configuration._to_dict()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """
        Create User from dictionary.
        
        Args:
            data: Dictionary with user data
            
        Returns:
            Reconstructed User instance
        """
        collection_data = data.get('collection', {})
        collection = Collection.from_dict(collection_data)
        
        config_data = data.get('configuration', {})
        configuration = Configuration.from_dict(config_data)
        
        user = cls(
            name=data['name'],
            email=data['email'],
            collection=collection,
            configuration=configuration
        )
        
        return user
