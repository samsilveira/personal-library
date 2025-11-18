"""
Module containing the Publication class and its specializations.
"""

class Publication:
    """
    Abstract class representing a publication in the library.

    Responsible for managing information and status of a publication, including bibliographic data, reading status, rating, and annotations.

    Attributes:
        id (str): Unique identifier of the publication
        title (str): Title of the publication
        author (str): Author's name
        publisher (str): Publisher's name
        year (int): Year of publication
        genre (str): Literary genre
        number_of_pages (int): Number of pages
        type (str): Type of publication (Book/Magazine)
        file_path (str): Path to the digital file
        status (str): Current status (UNREAD, READING, READ)
        start_read_date (Optional[date]): Start date of reading
        end_read_date (Optional[date]): End date of reading
        rating (Optional[float]): Score from 0 to 10
        rating_inclusion_date (Optional[date]): Date of the rating
        annotations (list): List of associated annotations
        
    """

    def __init__(self):
        """Initializes a new publication."""
        pass

    def start_reading(self):
        """
        Starts reading the publication.
        
        Updates the status to READING and registers the start date.
        """
        pass

    def finish_reading(self):
        """
        Finishes reading the publication.

        Validates if there is a start date and updates status to READ.

        Raises:
            ValueError: If there is no reading start date.
        """
        pass

    def rate_publication(self, rating: float):
        """
        Registers a rating for the publication.

        Args:
            rating: Value between 0 and 10

        Raises:
            ValueError: If status is not READ or rating is invalid.
        """
        pass

    def add_annotation(self, annotation):
        """
        Adds a note to the publication.

        Args:
            annotation: Annotation object to be added
        """
        pass

    def list_annotations(self):
        """
        Returns all annotations of the publication.

        Returns:
            List of Annotation objects
        """
        pass

    def remove_annotation(self, annotation_id: str):
        """
        Removes an annotation by ID.

        Args:
            annotation_id: Identifier of the annotation

        Returns:
            True if successfully removed, False otherwise
        """
        pass

class Book(Publication):
    """
    Represents a book in the library.

    Specialization of Publication with ISBN.

    Attributes:
        isbn (str): ISBN code of the book
    """

    def __init__(self):
        """Initializes a new book."""
        super().__init__()

class Magazine(Publication):
    """
    Represents a magazine in the library.

    Specialization of Publication with ISSN.

    Attributes:
        issn (str): ISSN code of the magazine
    """

    def __init__(self):
        """Initializes a new magazine."""
        super().__init__()

