import pytest
from models import Book, Report, Collection

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
        collection.add_publication(book)
    
    return collection