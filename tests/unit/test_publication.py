"""
Unit tests for Publication class.
"""

import pytest
from datetime import date
from src.models import Book, Annotation

class TestPublication:
    """Test cases for Publication (using Book as concrete implementation)."""

    def test_create_publication(self, sample_book):
        """Test creating a publication."""
        assert sample_book.id == 1
        assert sample_book.title == "1984"
        assert sample_book.author == "George Orwell"
        assert sample_book.year == 1949
        assert sample_book.status == "UNREAD"

    def test_invalid_id_raises_error(self):
        """Test that invalid ID raises ValueError."""
        with pytest.raises(ValueError, match="ID must be a positive integer"):
            Book(
                pub_id=0,
                title="Teste",
                author="Autor",
                publisher="Editora",
                year=2025,
                genre="Gênero",
                number_of_pages=100
            )

    def test_empty_title_raises_error(self):
        """Test that empty title raises ValueError."""
        with pytest.raises(ValueError, match="Title cannot be empty"):
            Book(
                pub_id=1,
                title="",
                author="Autor",
                publisher="Editora",
                year=2025,
                genre="Gênero",
                number_of_pages=100
            )

    def test_invalid_year_raises_error(self):
        """Test that year < 1500 raises ValueError."""
        with pytest.raises(ValueError, match="Year must be greater than or equal to 1500"):
            Book(
                pub_id=1,
                title="Título",
                author="Autor",
                publisher="Editora",
                year=1400,
                genre="Gênero",
                number_of_pages=100
            )
    
    def test_start_reading(self, sample_book):
        """Test starting to read a publication."""
        sample_book.start_reading()

        assert sample_book.status == "READING"
        assert sample_book.start_read_date == date.today()

    def test_start_reading_twice_raises_error(self, sample_book):
        """Test that starting reading twice raises ValueError."""
        sample_book.start_reading()

        with pytest.raises(ValueError, match="Publication already has READING status"):
            sample_book.start_reading()

    def test_finish_reading(self, sample_book):
        """Test finishing reading a publication."""
        sample_book.start_reading()
        sample_book.finish_reading()

        assert sample_book.status == "READ"
        assert sample_book.end_read_date == date.today()

    def test_finish_reading_without_starting_raises_error(self, sample_book):
        """Test that finishing a book withou starting raises ValueError."""
        with pytest.raises(ValueError, match="Publication cannot be finalized without starting reading"):
            sample_book.finish_reading()

    def test_rate_publication(self, sample_book):
        """Test rating a publication."""
        sample_book.start_reading()
        sample_book.finish_reading()
        sample_book.rate_publication(9.5)

        assert sample_book.rating == 9.5
        assert sample_book.rating_inclusion_date == date.today()

    def test_rate_unfinished_publication_raises_error(self, sample_book):
        """Test that rating unfinished publication raises ValueError."""
        with pytest.raises(ValueError, match="Publication cannot be evaluated without finishing reading"):
            sample_book.rate_publication(9.0)

    @pytest.mark.parametrize("invalid_rating", [-1, 11, 15.5])
    def test_invalid_rating_raises_error(self, sample_book, invalid_rating):
        """Test that invalid rating raises ValueError."""
        sample_book.start_reading()
        sample_book.finish_reading()

        with pytest.raises(ValueError, match="The rating cannot be less than 0 or greater than 10"):
            sample_book.rate_publication(invalid_rating)

    def test_add_annotation(self, sample_book, sample_annotation):
        """Test adding an annotation."""
        sample_book.add_annotation(sample_annotation)

        assert len(sample_book.list_annotations()) == 1
        assert sample_book.list_annotations()[0] == sample_annotation

    def test_add_invalid_annotation_raises_error(self, sample_book):
        """Test that adding non-Annotation raises TypeError."""
        with pytest.raises(TypeError, match="must be an Annotation instance"):
            sample_book.add_annotation("não é anotação")

    def test_remove_annotation(self, sample_book, sample_annotation):
        """Test removing an annotation."""
        sample_book.add_annotation(sample_annotation)
        result = sample_book.remove_annotation(sample_annotation.id)

        assert result is True
        assert len(sample_book.list_annotations()) == 0

    def test_remove_nonexisting_annotation(self, sample_book):
        """Test removing non-existing annotation returns False"""
        result = sample_book.remove_annotation("id_inexistente")
        assert result is False

    def test_publication_equality(self):
        """Test publication equality based on title and author."""
        book1 = Book(1, "Teste", "Autor", "Editora", 2025, "Gênero", 100)
        book2 = Book(2, "Teste", "Autor", "Editora", 2025, "Gênero", 100)
        book3 = Book(3, "Diferente", "Autor", "Editora", 2025, "Gênero", 100)

        assert book1 == book2
        assert book1 != book3

    def test_publication_comparison(self):
        """Test publication comparison by year."""
        book1 = Book(1, "Livro Antigo", "Autor", "Editora", 1900, "Gênero", 100)
        book2 = Book(2, "Livro Novo", "Autor", "Editora", 2000, "Gênero", 100)

        assert book1 < book2
        assert not book2 < book1