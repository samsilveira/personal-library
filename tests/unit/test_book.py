"""
Unit tests for Book class.
"""

import pytest
from src.models import Book

class TestBook:
    """Test cases specific to Book class."""

    def test_create_book_with_isbn(self):
        """Test creating a book with ISBN."""
        book = Book(
            pub_id=1,
            title="Livro Teste",
            author="Autor Teste",
            publisher="Editora Teste",
            year=2025,
            genre="Ficção",
            number_of_pages=300,
            isbn="978-3-16-148410-0",
            edition=2
        )

        assert book.isbn == "978-3-16-148410-0"
        assert book.edition == 2
    
    def test_create_book_without_isbn(self):
        """Test creating a book without ISBN (Optional)."""
        book = Book(
            pub_id=1,
            title="Livro Teste",
            author="Autor Teste",
            publisher="Editora Teste",
            year=2025,
            genre="Ficção",
            number_of_pages=300
        )

        assert book.isbn == ""
        assert book.edition == 1

    def test_book_with_digital_file(self):
        """Test book with digital file path."""
        book = Book(
            pub_id=1,
            title="Livro Digital",
            author="Autor Teste",
            publisher="Editora Teste",
            year=2025,
            genre="Ficção",
            number_of_pages=300,
            file_path="/caminho/pro/livro.pdf"
        )

        assert book.file_path == "/caminho/pro/livro.pdf"
        assert book.has_digital_file() is True

    def test_book_to_dict(self, sample_book):
        """Test book serialization."""
        data = sample_book.to_dict()

        assert data['type'] == 'Book'
        assert data['title'] == "1984"
        assert data['isbn'] == "978-0452284234"
        assert data['edition'] == 1

    def test_book_from_dict(self):
        """Test book deserialization."""
        data = {
            'type': 'Book',
            'pub_id': 5,
            'title': 'Livro Reconstruído',
            'author': 'Autor',
            'publisher': 'Editora',
            'year': 2025,
            'genre': 'Ficção',
            'number_of_pages': 250,
            'isbn': '123-456789',
            'edition': 3,
            'file_path': '/livros/teste.pdf',
            'status': 'UNREAD',
            'start_read_date': None,
            'end_read_date': None,
            'rating': None,
            'rating_inclusion_date': None,
            'annotations': []
        }
        
        book = Book.from_dict(data)
        
        assert book.id == 5
        assert book.title == 'Livro Reconstruído'
        assert book.isbn == '123-456789'
        assert book.edition == 3
        assert book.file_path == '/livros/teste.pdf'

    def test_book_str_includes_isbn(self, sample_book):
        """Test that string representation includes ISBN."""
        str_repr = str(sample_book)

        assert "ISBN: 978-0452284234" in str_repr