"""
Unit tests for Magazine class.
"""

import pytest
from src.models import Magazine

class TestMagazine:
    """Test cases specific to Magazine class."""
    
    def test_create_magazine_with_issn(self):
        """Test creating a magazine with ISSN."""
        magazine = Magazine(
            pub_id=1,
            title="Scientific American",
            author="Various",
            publisher="Springer Nature",
            year=2025,
            genre="Science",
            number_of_pages=100,
            issue_number=12,
            issn="0036-8733"
        )
        
        assert magazine.issue_number == 12
        assert magazine.issn == "0036-8733"
    
    def test_create_magazine_without_issn(self):
        """Test creating a magazine without ISSN (optional)."""
        magazine = Magazine(
            pub_id=1,
            title="Revista Teste",
            author="Autores",
            publisher="Editora",
            year=2025,
            genre="Geral",
            number_of_pages=80,
            issue_number=5
        )
        
        assert magazine.issn == ""
    
    def test_invalid_issue_number_raises_error(self):
        """Test that invalid issue number raises ValueError."""
        with pytest.raises(ValueError, match="Issue number must be positive"):
            Magazine(
                pub_id=1,
                title="Revista",
                author="Diversos",
                publisher="Editora",
                year=2025,
                genre="Geral",
                number_of_pages=100,
                issue_number=0
            )
        
        with pytest.raises(ValueError, match="Issue number must be positive"):
            Magazine(
                pub_id=1,
                title="Revista",
                author="Autores",
                publisher="Editora",
                year=2025,
                genre="Geral",
                number_of_pages=100,
                issue_number=-1
            )
    
    def test_magazine_to_dict(self, sample_magazine):
        """Test magazine serialization."""
        data = sample_magazine.to_dict()
        
        assert data['type'] == 'Magazine'
        assert data['title'] == "National Geographic"
        assert data['issue_number'] == 145
        assert data['issn'] == "0027-9358"
    
    def test_magazine_from_dict(self):
        """Test magazine deserialization."""
        data = {
            'type': 'Magazine',
            'pub_id': 5,
            'title': 'Revista Reconstruída',
            'author': 'Autores',
            'publisher': 'Editora',
            'year': 2025,
            'genre': 'Tecnologia',
            'number_of_pages': 120,
            'issue_number': 42,
            'issn': '1234-5678',
            'status': 'UNREAD',
            'start_read_date': None,
            'end_read_date': None,
            'rating': None,
            'rating_inclusion_date': None,
            'annotations': []
        }
        
        magazine = Magazine.from_dict(data)
        
        assert magazine.id == 5
        assert magazine.title == 'Revista Reconstruída'
        assert magazine.issue_number == 42
        assert magazine.issn == '1234-5678'
    
    def test_magazine_str_includes_issue(self, sample_magazine):
        """Test that string representation includes issue number."""
        str_repr = str(sample_magazine)
        assert "ISSN: 0027-9358" in str_repr