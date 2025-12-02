import pytest
from models import Book

@pytest.fixture
def sample_book():
    """Creates and returns a Book instance for testing."""
    return Book(
        pub_id=3,
        title="Memórias Póstumas de Brás Cubas",
        author="Machado de Assis",
        publisher="Editora FTD",
        year=2010,
        genre="Literatura experimental",
        number_of_pages=320,
        isbn="978-8532275226"
        
    )

@pytest.fixture
def Book_cls():
    """Returns the Book class to be injected into tests that need to instantiate an object."""
    return Book
