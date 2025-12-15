"""
Unit tests for Annotation class.
"""

import pytest
from datetime import date
from src.models import Annotation

class TestAnnotation:
    """Test cases for Annotation class."""

    def test_create_annotation(self):
        """Test creating a basic annotation."""
        ann = Annotation(
            annotation_id="ann_001",
            text="Bela reflexão",
            reference_excerpt="Referência 1"
        )

        assert ann.id == "ann_001"
        assert ann.text == "Bela reflexão"
        assert ann.reference_excerpt == "Referência 1"
        assert isinstance(ann.date, date)

    def test_annotation_str_representation(self):
        """Test string representation."""
        ann = Annotation("ann_002", "Ponto importante", "Referência 2")
        str_repr = str(ann)

        assert "Ponto importante" in str_repr
        assert "Referência 2" in str_repr

    def test_annotation_to_dict(self):
        """Test serialization to dictionary."""
        ann = Annotation("ann_003", "Rever este trecho", "Referência 3")
        data = ann.to_dict()

        assert data['annotation_id'] == "ann_003"
        assert data['text'] == "Rever este trecho"
        assert data['reference_excerpt'] == "Referência 3"
        assert 'date' in data
        
    def test_annotation_from_dict(self):
        """Test deserialization from dictionary."""
        data = {
            'annotation_id': "ann_004",
            'text': "Anotação reconstruída",
            'reference_excerpt': "Referência 4",
            'date': "2025-12-15"
        }

        ann = Annotation.from_dict(data)

        assert ann.id == "ann_004"
        assert ann.text == "Anotação reconstruída"
        assert ann.reference_excerpt == "Referência 4"
        assert ann.date == date.fromisoformat("2025-12-15")

    def test_empty_text_raises_error(self):
        """Test that empty text raises ValueError"""
        with pytest.raises(ValueError, match="Text cannot be empty"):
            Annotation("ann_005", "")