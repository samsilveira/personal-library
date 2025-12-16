"""
Unit tests for Collection class.
"""

import pytest
from datetime import date, timedelta
from src.models import Collection, Book, Configuration


class TestCollection:
    """Test cases for Collection class."""
    
    def test_create_empty_collection(self):
        """Test creating an empty collection."""
        collection = Collection()
        assert len(collection.list_publications()) == 0
    
    def test_register_publication(self, sample_book):
        """Test registering a publication."""
        collection = Collection()
        result = collection.register_publication(sample_book)
        
        assert result is True
        assert len(collection.list_publications()) == 1
    
    def test_register_duplicate_raises_error(self, sample_book):
        """Test that registering duplicate raises ValueError."""
        collection = Collection()
        collection.register_publication(sample_book)
        
        duplicate = Book(
            pub_id=99,
            title="1984",
            author="George Orwell",
            publisher="Secker & Warburg",
            year=1949,
            genre="Dystopian Fiction",
            number_of_pages=328
        )
        
        with pytest.raises(ValueError, match="already exists"):
            collection.register_publication(duplicate)
    
    def test_register_invalid_type_raises_error(self):
        """Test that registering non-Publication raises TypeError."""
        collection = Collection()
        
        with pytest.raises(TypeError, match="Must provide a Publication instance"):
            collection.register_publication("not a publication")
    
    def test_remove_publication(self, sample_collection, sample_book, sample_magazine):
        """Test removing a publication."""
        result = sample_collection.remove_publication(1)
        
        assert result is True
        assert len(sample_collection.list_publications()) == 1
    
    def test_remove_nonexistent_publication(self, sample_collection):
        """Test removing non-existent publication returns False."""
        result = sample_collection.remove_publication(999)
        assert result is False
    
    def test_search_by_author(self, sample_collection):
        """Test searching by author."""
        results = sample_collection.search_by_author("Orwell")
        
        assert len(results) == 1
        assert results[0].title == "1984"
    
    def test_search_by_author_case_insensitive(self, sample_collection):
        """Test that author search is case-insensitive."""
        results = sample_collection.search_by_author("orwell")
        assert len(results) == 1
    
    def test_search_by_title(self, sample_collection):
        """Test searching by title."""
        results = sample_collection.search_by_title("1984")
        
        assert len(results) == 1
        assert results[0].author == "George Orwell"
    
    def test_search_by_status(self, collection_with_mixed_status):
        """Test searching by status."""
        unread = collection_with_mixed_status.search_by_status("UNREAD")
        reading = collection_with_mixed_status.search_by_status("READING")
        read = collection_with_mixed_status.search_by_status("READ")
        
        assert len(unread) == 1
        assert len(reading) == 1
        assert len(read) == 1
    
    def test_filter_by_reading_period(self):
        """Test filtering publications by reading period."""
        collection = Collection()
        
        book1 = Book(1, "Recent", "Author", "Pub", 2020, "Fiction", 100)
        book1.start_reading()
        book1.finish_reading()
        
        book2 = Book(2, "Older", "Author", "Pub", 2020, "Fiction", 100)
        book2.start_reading()
        book2._end_read_date = date.today() - timedelta(days=10)
        book2._Publication__status = "READ"
        
        collection.register_publication(book1)
        collection.register_publication(book2)
        
        start = date.today() - timedelta(days=7)
        end = date.today()
        results = collection.filter_by_reading_period(start, end)
        
        assert len(results) == 1
        assert results[0].title == "Recent"
    
    def test_start_publication_reading(self, sample_collection, sample_configuration):
        """Test starting to read a publication through collection."""
        result = sample_collection.start_publication_reading(1, sample_configuration)
        
        assert result is True
        pubs = sample_collection.list_publications()
        book = next(p for p in pubs if p.id == 1)
        assert book.status == "READING"
    
    def test_start_reading_exceeds_limit_raises_error(self, sample_configuration):
        """Test that exceeding simultaneous reading limit raises ValueError."""
        collection = Collection()
        sample_configuration.simultaneous_reading_limit = 2
        
        for i in range(1, 4):
            book = Book(i, f"Book {i}", "Author", "Pub", 2020, "Fiction", 100)
            collection.register_publication(book)
        
        collection.start_publication_reading(1, sample_configuration)
        collection.start_publication_reading(2, sample_configuration)
        
        with pytest.raises(ValueError, match="Maximum number of simultaneous readings reached"):
            collection.start_publication_reading(3, sample_configuration)
    
    def test_start_reading_nonexistent_publication_raises_error(self, sample_collection, sample_configuration):
        """Test starting reading of non-existent publication raises ValueError."""
        with pytest.raises(ValueError, match="not found"):
            sample_collection.start_publication_reading(999, sample_configuration)