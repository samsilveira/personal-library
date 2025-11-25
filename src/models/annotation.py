"""
Module containing the Annotation class.
"""

from typing import Optional
from datetime import date

class Annotation:
    """
    Represents a text note associated with a publication.

    Annotations are completely dependent on their parent publications's lifecycle.

    Attributes:
        id (str): Unique identifier for the annotation
		date (date): Date when the annotation was created
		reference_excerpt (Optional[str]): Text excerpt being refenced
		text (str): The annotation content itself
    """

    def __init__(self, annotation_id: str, text: str, reference_excerpt: Optional[str] = None):
        """
        Initialize a new annotation.

        Args:
            annotation_id: Unique identifier
            text: Annotation content
            reference_excerpt: Optional text excerpt being referenced
        """
        self.__id = annotation_id
        self._text = None
        self.text = text
        self._reference_excerpt = reference_excerpt
        self._date = date.today()

    def __str__(self):
        excerpt = f" [Ref.: {self._reference_excerpt[:30]}...]" if self._reference_excerpt else ""
        return f"[{self._date}]{excerpt} {self._text[:50]}..."

    @property
    def id(self):
        return self.__id

    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value: str):
        """Defines the text of the annotation with validation."""
        if not value or not value.strip():
            raise ValueError("Text cannot be empty")
        self._text = value.strip()