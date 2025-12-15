"""
Pytest configuration and shared fixtures.
"""

import pytest
from datetime import date
from src.models import Book, Magazine, Annotation, Report, Collection, Configuration, User
from data import repository

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
    """Create a collection with sample books."""
    collection = Collection()
    
    # 2 UNREAD (não precisa fazer nada, já é o padrão)
    book1 = Book(
        pub_id=1, 
        title="Book 1", 
        author="Author 1", 
        publisher="Pub 1",
        year=2020, 
        genre="Fiction", 
        number_of_pages=200, 
        isbn="111"
    )
    # ✅ book1 já está como UNREAD por padrão
    
    book2 = Book(
        pub_id=2, 
        title="Book 2", 
        author="Author 2", 
        publisher="Pub 2",
        year=2021, 
        genre="Fiction", 
        number_of_pages=300, 
        isbn="222"
    )
    # ✅ book2 já está como UNREAD por padrão
    
    # 1 READING
    book3 = Book(
        pub_id=3, 
        title="Book 3", 
        author="Author 3", 
        publisher="Pub 3",
        year=2022, 
        genre="Fiction", 
        number_of_pages=250, 
        isbn="333"
    )
    # ✅ Usar _restore_state para definir como READING
    book3._restore_state(
        status="READING",
        start_date=date(2024, 1, 1),
        end_date=None,
        rating=None,
        rating_date=None,
        annotations=[]
    )
    
    # 2 READ (com ratings)
    book4 = Book(
        pub_id=4, 
        title="Book 4", 
        author="Author 4", 
        publisher="Pub 4",
        year=2023, 
        genre="Fiction", 
        number_of_pages=400, 
        isbn="444"
    )
    # ✅ Usar _restore_state para definir como READ com rating
    book4._restore_state(
        status="READ",
        start_date=date(2024, 1, 1),
        end_date=date(2024, 2, 1),
        rating=8.5,
        rating_date=date(2024, 2, 1),
        annotations=[]
    )
    
    book5 = Book(
        pub_id=5, 
        title="Book 5", 
        author="Author 5", 
        publisher="Pub 5",
        year=2024, 
        genre="Fiction", 
        number_of_pages=350, 
        isbn="555"
    )
    # ✅ Usar _restore_state para definir como READ com rating
    book5._restore_state(
        status="READ",
        start_date=date(2024, 1, 15),
        end_date=date(2024, 2, 15),
        rating=9.0,
        rating_date=date(2024, 2, 15),
        annotations=[]
    )
    
    for book in [book1, book2, book3, book4, book5]:
        collection.register_publication(book)
    
    return collection