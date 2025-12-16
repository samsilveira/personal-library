"""
Unit tests for User class.
"""

import pytest
from datetime import date
from src.models import User, Collection, Configuration, Book


class TestUser:
    """Test cases for User class."""
    
    def test_create_user(self):
        """Test creating a basic user."""
        user = User(name="Fulano de Tal", email="fulano@exemplo.com")
        
        assert user.name == "Fulano de Tal"
        assert user.email == "fulano@exemplo.com"
        assert isinstance(user.collection, Collection)
        assert isinstance(user.configuration, Configuration)
    
    def test_empty_name_raises_error(self):
        """Test that empty name raises ValueError."""
        with pytest.raises(ValueError, match="Name cannot be empty"):
            User(name="", email="test@example.com")
    
    def test_invalid_email_raises_error(self):
        """Test that invalid email raises ValueError."""
        with pytest.raises(ValueError, match="Invalid email format"):
            User(name="Test User", email="invalid-email")
        
        with pytest.raises(ValueError, match="Invalid email format"):
            User(name="Test User", email="@example.com")
        
        with pytest.raises(ValueError, match="Invalid email format"):
            User(name="Test User", email="user@")
    
    def test_user_with_custom_collection(self):
        """Test user with custom collection."""
        collection = Collection()
        book = Book(1, "Test", "Author", "Pub", 2020, "Fiction", 100)
        collection.register_publication(book)
        
        user = User(name="Test", email="test@example.com", collection=collection)
        
        assert len(user.collection.list_publications()) == 1
    
    def test_user_with_custom_configuration(self):
        """Test user with custom configuration."""
        config = Configuration()
        config.annual_goal = 50
        
        user = User(name="Test", email="test@example.com", configuration=config)
        
        assert user.configuration.annual_goal == 50
    
    def test_user_to_dict(self):
        """Test user serialization."""
        sample_user = User(name="Test User", email="test@example.com")
        data = sample_user.to_dict()
        
        assert data['name'] == "Test User"
        assert data['email'] == "test@example.com"
        assert 'collection' in data
        assert 'configuration' in data
    
    def test_user_from_dict(self):
        """Test user deserialization."""
        data = {
            'name': 'Reconstructed User',
            'email': 'reconstructed@example.com',
            'collection': {
                'publications': []
            },
            'configuration': {
                'annual_goal': 15,
                'simultaneous_reading_limit': 3,
                'favorite_genre': 'Fiction'
            }
        }
        
        user = User.from_dict(data)
        
        assert user.name == 'Reconstructed User'
        assert user.email == 'reconstructed@example.com'
        assert user.configuration.annual_goal == 15