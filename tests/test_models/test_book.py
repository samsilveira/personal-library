import pytest

def test_book_creation_with_valid_data(sample_book):
    """Test that a book is created correctly with valid data."""
    assert sample_book.id == 3
    assert sample_book.title == "Memórias Póstumas de Brás Cubas"
    assert sample_book.author == "Machado de Assis"
    assert sample_book.publisher == "Editora FTD"
    assert sample_book.year == 2010
    assert sample_book.genre == "Literatura experimental"
    assert sample_book.number_of_pages == 320
    assert sample_book.isbn == "978-8532275226"

def test_book_default_values(Book_cls):
    """Test that default values are set correctly."""
    book = Book_cls(
        pub_id=1,
        title="Test Book",
        author="Test Author",
        publisher="Test Publisher",
        year=2025,
        genre="Test Genre",
        number_of_pages=100,
        isbn="123456789"
    )

    assert book.status == "UNREAD"
    assert book.rating is None
    assert book.start_read_date is None
    assert book.end_read_date is None
    assert book.rating_inclusion_date is None
    assert book.annotations == []

def test_book_with_optional_parameters(Book_cls):
    """Test creating a book with optional parameters."""
    book = Book_cls(
        pub_id=2,
        title="1984",
        author="George Orwell",
        publisher="Companhia das Letras",
        year=2009,
        genre="Ficção Distópica",
        number_of_pages=416,
        isbn="978-8535914849",
        edition=3
    )

    assert book.edition == 3


def test_invalid_pages_negative(Book_cls):
    """Test that negative pages raise ValueErros."""
    with pytest.raises(ValueError) as exc_info:
        Book_cls(
            pub_id=4,
            title="Test",
            author="Test",
            publisher="Test",
            year=2025,
            genre="Test",
            number_of_pages=-232,
            isbn="123"
        )
    
    assert "greater than zero" in str(exc_info.value).lower()

def test_invalid_pages_zero(Book_cls):
    """Test that zero pages raise ValueError."""
    with pytest.raises(ValueError) as exc_info:
        Book_cls(
            pub_id=5,
            title="Test",
            author="Test",
            publisher="Test",
            year=2025,
            genre="Test",
            number_of_pages=0,
            isbn="123"
        )
    
    assert "greater than zero" in str(exc_info.value).lower()

def change_pages_to_invalid_value(sample_book):
    """Test that changing pages to invalid value raises error."""
    with pytest.raises(ValueError):
        sample_book.number_of_pages = -50

    assert sample_book.number_of_pages == 320

def test_start_reading(sample_book):
    """Test start to read a book."""
    assert sample_book.status == "UNREAD"

    sample_book.start_reading()

    assert sample_book.status == "READING"
    assert sample_book.start_read_date is not None

def test_finish_reading(sample_book):
    """Test finishing a book."""
    sample_book.start_reading()

    sample_book.finish_reading()

    assert sample_book.status == "READ"
    assert sample_book.end_read_date is not None

def test_add_rating(sample_book):
    """Test adding a rating to a book."""
    sample_book.start_reading()
    sample_book.finish_reading()

    sample_book.rate_publication(4.5)

    assert sample_book.rating == 4.5

def test_invalid_rating_range(sample_book):
    """Test adding a invalid rating to a book."""
    sample_book.start_reading()
    sample_book.finish_reading()

    with pytest.raises(ValueError):
        sample_book.rate_publication(11)

    with pytest.raises(ValueError):
        sample_book.rate_publication(-1)

def test_cannot_rate_unfinished_book(sample_book):
    """Test adding a invalid rating to a book."""
    with pytest.raises(ValueError) as exc_info:
        sample_book.rate_publication(5)
    assert "finishing" in str(exc_info.value).lower()

    sample_book.start_reading()
    with pytest.raises(ValueError) as exc_info:
        sample_book.rate_publication(5)
    assert "finishing" in str(exc_info.value).lower()

