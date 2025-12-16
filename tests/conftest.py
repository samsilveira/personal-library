"""
Pytest configuration and shared fixtures.
"""

import pytest
from datetime import date
from src.models import Book, Magazine, Annotation, Report, Collection, Configuration, User
from src.data import repository

@pytest.fixture
def sample_book():
    """Creates and returns a Book instance for testing."""
    return Book(
        pub_id=1,
        title="1984",
        author="George Orwell",
        publisher="Secker & Warburg",
        year=1949,
        genre="Dystopian Fiction",
        number_of_pages=328,
        isbn="978-0452284234"
    )

@pytest.fixture
def sample_magazine():
    """Create a sample magazine for testing."""
    return Magazine(
        pub_id=2,
        title="National Geographic",
        author="Various authors",
        publisher="National Geographic Society",
        year=2025,
        genre="Science",
        number_of_pages=120,
        issue_number=145,
        issn="0027-9358"
    )

@pytest.fixture
def sample_collection():
    """Create a collection with sample publications."""
    collection = Collection()

    book = Book(
        pub_id=1,
        title="1984",
        author="George Orwell",
        publisher="Secker & Warburg",
        year=1949,
        genre="Dystopian Fiction",
        number_of_pages=328,
        isbn="978-0452284234"
    )

    magazine = Magazine(
        pub_id=2,
        title="National Geographic",
        author="Various authors",
        publisher="National Geographic Society",
        year=2025,
        genre="Science",
        number_of_pages=120,
        issue_number=145,
        issn="0027-9358"
    )

    collection.register_publication(book)
    collection.register_publication(magazine)
    return collection

@pytest.fixture
def sample_configuration():
    """Create a sample configuration."""
    config = Configuration()
    config.annual_goal = 12
    config.simultaneous_reading_limit = 3
    return config

@pytest.fixture
def sample_user():
    """Create a sample user with collection and configuration."""
    user = User(name="User Teste",email="teste@exemplo.com")
    user.collection = sample_collection
    user.configuration = sample_configuration
    return user

@pytest.fixture
def sample_annotation():
    """Create a sample annotation."""
    return Annotation(
        annotation_id="ann_001",
        text="Isso é um teste de anotação",
        reference_excerpt="Excerto de referência teste"
    )

@pytest.fixture
def read_book():
    """Create a book that has been read an rated."""
    book = Book(
        pub_id=3,
        title="Senhor dos Anéis",
        author="J.R.R. Tolkien",
        publisher="Harper Collins",
        year=2019,
        genre="Fantasy",
        number_of_pages=1216,
        isbn="978-0618574984",
        edition=1
    )
    book.start_reading()
    book.finish_reading()
    book.rate_publication(10)
    return book

@pytest.fixture
def collection_with_mixed_status():
    """Create a collection with publications in different statuses."""
    collection = Collection()

    unread = Book(
        pub_id=1,
        title="Livro não lido",
        author="Autor Um",
        publisher="Editora",
        year=2025,
        genre="Ficção",
        number_of_pages=300
    )

    reading = Book(
        pub_id=2,
        title="Livro Em Leitura",
        author="Autor Dois",
        publisher="Editora",
        year=2024,
        genre="Ficção",
        number_of_pages=400
    )
    reading.start_reading()

    read = Book(
        pub_id=3,
        title="Livro Lido",
        author="Autor Três",
        publisher="Editora",
        year=2023,
        genre="Ficção",
        number_of_pages=500
    )
    read.start_reading()
    read.finish_reading()
    read.rate_publication(8.7)

    collection.register_publication(unread)
    collection.register_publication(reading)
    collection.register_publication(read)

    return collection

@pytest.fixture
def Book_cls():
    """Returns the Book class to be injected into tests that need to instantiate an object."""
    return Book

@pytest.fixture
def empty_collection():
    """Create an empty collection."""
    return Collection()

@pytest.fixture
def populated_collection():
    """
    Create a collection with 5 publications in different states:
    - 2 UNREAD
    - 1 READING
    - 2 READ (with ratings 8.5 and 9.0)
    """
    collection = Collection()
    
    book1 = Book(1, "Livro Não Lido 1", "Autor A", "Editora", 2025, "Ficção", 300)
    book2 = Book(2, "Livro Não Lido 2", "Autor B", "Editora", 2025, "Ciência", 250)
    
    book3 = Book(3, "Livro em Leitura", "Autor C", "Editora", 2024, "História", 400)
    book3.start_reading()
    
    book4 = Book(4, "Livro Lido 1", "Autor D", "Editora", 2024, "Biografia", 350)
    book4.start_reading()
    book4.finish_reading()
    book4.rate_publication(8.5)
    
    book5 = Book(5, "Livro Lido 2", "Autor E", "Editora", 2023, "Fantasia", 500)
    book5.start_reading()
    book5.finish_reading()
    book5.rate_publication(9.0)
    
    collection.register_publication(book1)
    collection.register_publication(book2)
    collection.register_publication(book3)
    collection.register_publication(book4)
    collection.register_publication(book5)
    
    return collection

@pytest.fixture
def collection_for_annual_goal():
    """Create a collection with books read in current year."""
    collection = Collection()
    current_year = date.today().year
    
    for i in range(1, 4):
        book = Book(i, f"Livro {i}", f"Autor {i}", "Editora", current_year, "Ficção", 300)
        book.start_reading()
        book.finish_reading()
        collection.register_publication(book)
    
    old_book = Book(4, "Livro Antigo", "Autor", "Editora", current_year - 1, "Ficção", 200)
    old_book.start_reading()
    old_book.finish_reading()
    old_book._end_read_date = date(current_year - 1, 12, 15)
    collection.register_publication(old_book)
    
    return collection

@pytest.fixture
def collection_with_ratings():
    """
    Create a collection with multiple rated books for evaluation testing.
    Ratings: 7.0, 8.5, 9.0, 6.5, 10.0
    """
    collection = Collection()

    ratings = [7.0, 8.5, 9.0, 6.5, 10.0]
    for i, rating in enumerate(ratings, start=1):
        book = Book(
            pub_id=i,
            title=f"Livro avaliado {i}",
            author=f"Autor {i}",
            publisher="Editora",
            year=2021 + i,
            genre="Ficção",
            number_of_pages=200 + (i * 50)
        )
        book.start_reading()
        book.finish_reading()
        book.rate_publication(rating)
        collection.register_publication(book)

    return collection

@pytest.fixture
def sample_configuration():
    """Create a sample configuration with annual goal."""
    config = Configuration()
    config.annual_goal = 12
    config.simultaneous_reading_limit = 3
    return config
