"""
Module containing the Annotation class.
"""

from typing import Optional

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

        pass