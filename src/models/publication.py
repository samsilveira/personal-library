"""
Module containing the Publication class and its specializations.
"""

from datetime import date
from abc import ABC
from .annotation import Annotation
from .mixins import DigitalAsset

class Publication(ABC):
    """
    Abstract class representing a publication in the library.

    Responsible for managing information and status of a publication, including bibliographic data, reading status, rating, and annotations.

    Attributes:
        id (int): Unique identifier of the publication
        title (str): Title of the publication
        author (str): Author's name
        publisher (str): Publisher's name
        year (int): Year of publication
        genre (str): Literary genre
        number_of_pages (int): Number of pages
        type (str): Type of publication (Book/Magazine)
        status (str): Current status (UNREAD, READING, READ)
        start_read_date (Optional[date]): Start date of reading
        end_read_date (Optional[date]): End date of reading
        rating (Optional[float]): Score from 0 to 10
        rating_inclusion_date (Optional[date]): Date of the rating
        annotations (list): List of associated annotations
        
    """

    def __init__(self,
        pub_id: int,
        title: str,
        author: str,
        publisher: str,
        year: int,
        genre: str,
        number_of_pages: int,
        pub_type: str
    ):
        """
        Initializes a new publication.
        
        Args:
            pub_id: Unique identifier (must be positive integer)
            title: Title of the publication (cannot be empty)
            author: Author's name
            publisher: Publisher's name
            year: Year of publication (must be >= 1500)
            genre: Literary genre
            number_of_pages: Number of pages
            pub_type: Type of publication (Book/Magazine)
            
        Raises:
            ValueError: If pub_id is not a positive integer, title is empty, or year < 1500
        """
        if not isinstance(pub_id, int) or pub_id <= 0:
            raise ValueError("ID must be a positive integer")
        self.__id = pub_id

        self.title = title       

        self.year = year
        
        self._author = author
        self._publisher = publisher
        self._genre = genre
        self._number_of_pages = number_of_pages
        self._pub_type = pub_type
        
        self.__status = "UNREAD"
        self._start_read_date = None
        self._end_read_date = None
        self.__rating = None
        self._rating_inclusion_date = None
        self._annotations = []

    def __str__(self):
        """Returns a string representation of the publication."""
        return f"[{self.id}] {self.title} - {self._author}"
    
    def __repr__(self):
        """Returns a detailed representation of the publication for debugging."""
        return f"Publication(id={self.id}, title='{self.title}', year={self.year}, author='{self.author}', status='{self.status}')"
    
    def __eq__(self, other):
        """Checks equality based on title and author."""
        if not isinstance(other, Publication):
            return False
        return self.title == other.title and self.author == other.author
    
    def __lt__(self, other):
        """Compares publications by year for sorting."""
        if not isinstance(other, Publication):
            return NotImplemented
        return self.year < other.year

    @property
    def id(self):
        """Get publication ID."""
        return self.__id
    
    @property
    def title(self):
        """Get publication title."""
        return self._title
    
    @title.setter
    def title(self, value: str):
        """Set publication title with validation."""
        if not value or not value.strip():
            raise ValueError("Title cannot be empty")
        self._title = value.strip()

    @property
    def year(self):
        """Get publication year."""
        return self._year
    
    @year.setter
    def year(self, value: int):
        """Set publication year with validation."""
        if value < 1500:
            raise ValueError("Year must be greater than or equal to 1500")
        
        self._year = value

    @property
    def author(self):
        """Get publication's author."""
        return self._author
    
    @property
    def publisher(self):
        """Get publication's publisher."""
        return self._publisher

    @property
    def status(self):
        """Get publication's reading status."""
        return self.__status
    
    @property
    def rating(self):
        """Get publication's rating."""
        return self.__rating

    def start_reading(self):
        """
        Starts reading the publication.
        
        Updates the status to READING and registers the start date.
        If publication was already READ, resets rating and end date.
        
        Raises:
            ValueError: If publication already has READING status.
        """
        if self.__status == "READING":
            raise ValueError("Publication already has READING status")
        
        if self.__status == "READ":
            self._end_read_date = None
            self.__rating = None
            self._rating_inclusion_date = None
        
        self.__status = "READING"
        self._start_read_date = date.today()
        

    def finish_reading(self):
        """
        Finishes reading the publication.

        Validates if there is a start date and updates status to READ.

        Raises:
            ValueError: If there is no reading start date.
        """
        if self.__status != "READING" or self._start_read_date is None:
            raise ValueError("Publication cannot be finalized without starting reading")
        
        self.__status = "READ"
        self._end_read_date = date.today()

    @property
    def start_read_date(self):
        """Get start reading date."""
        return self._start_read_date
    
    @property
    def end_read_date(self):
        """Get end reading date."""
        return self._end_read_date

    def rate_publication(self, rating_value: float):
        """
        Registers a rating for the publication.

        Args:
            rating_value: Value between 0 and 10

        Raises:
            TypeError: If rating_value is not int or float.
            ValueError: If status is not READ or rating is invalid.
        """
        if not isinstance(rating_value, (int, float)):
            raise TypeError("The evaluation must be of int or float type")
        
        if self.__status != "READ":
            raise ValueError("Publication cannot be evaluated without finishing reading")
        
        if 0 > rating_value or rating_value > 10:
            raise ValueError("The rating cannot be less than 0 or greater than 10")

        self.__rating = rating_value
        self._rating_inclusion_date = date.today()

    def add_annotation(self, annotation: Annotation) -> None:
        """
        Adds a note to the publication.

        Args:
            annotation: Annotation object to be added

        Raises:
            TypeError: If the parameter is not an Annotation instance.
        """
        if not isinstance(annotation, Annotation):
            raise TypeError("The annotation must be an Annotation instance")
        
        self._annotations.append(annotation)

    def list_annotations(self):
        """
        Returns all annotations of the publication.

        Returns:
            List of Annotation objects (Shallow copy)
        """
        return self._annotations[:]

    def remove_annotation(self, annotation_id: str):
        """
        Removes an annotation by ID.

        Args:
            annotation_id: Identifier of the annotation

        Returns:
            True if successfully removed, False otherwise
        """
        for annotation in self._annotations:
            if annotation.id == annotation_id:
                self._annotations.remove(annotation)
                return True
        return False

class Book(Publication, DigitalAsset):
    """
    Represents a book in the library.

    Specialization of Publication with ISBN.

    Attributes:
        isbn (str): ISBN code of the book
        edition (int): Edition number
    """

    def __init__(self,
        pub_id,
        title,
        author,
        publisher,
        year,
        genre,
        number_of_pages,
        isbn="",
        edition=1,
        file_path=""
    ):
        """
        Initializes a new book.
        
        Args:
            pub_id: Unique identifier
            title: Book title
            author: Author's name
            publisher: Publisher's name
            year: Year of publication
            genre: Literary genre
            number_of_pages: Number of pages
            file_path: Path to the digital file (optional)
            isbn: ISBN code (optional)
            edition: Edition number (default: 1)
        """
        Publication.__init__(
            self,
            pub_id=pub_id, 
            title=title, 
            author=author, 
            publisher=publisher, 
            year=year, 
            genre=genre,
            number_of_pages=number_of_pages,
            pub_type="Book"
        )

        DigitalAsset.__init__(
            self,
            file_path=file_path
        )

        self._isbn = isbn
        self._edition = edition

    @property
    def isbn(self):
        """Get the book's ISBN."""
        return self._isbn
    
    @property
    def edition(self):
        """Get the book's edition."""
        return self._edition
    
    def __str__(self):
        """Returns a string representation of the book including ISBN."""
        return f"[{self.id}] {self.title} - {self._author} (ISBN: {self.isbn})"

class Magazine(Publication, DigitalAsset):
    """
    Represents a magazine in the library.

    Specialization of Publication with ISSN.

    Attributes:
        issn (str): ISSN code of the magazine
        issue_number (int): Magazine issue/edition number
    """

    def __init__(self,
        pub_id,
        title,
        author,
        publisher,
        year,
        genre,
        number_of_pages,
        issue_number,
        issn="",
        file_path=""
    ):
        """
        Initializes a new magazine.
        
        Args:
            pub_id: Unique identifier
            title: Magazine title
            author: Author's name
            publisher: Publisher's name
            year: Year of publication
            genre: Genre/category
            number_of_pages: Number of pages
            issue_number: Magazine issue/edition number
            file_path: Path to the digital file (optional)
            issn: ISSN code (optional)
        """
        Publication.__init__(
            self,
            pub_id=pub_id,
            title=title,
            author=author,
            publisher=publisher,
            year=year,
            genre=genre,
            number_of_pages=number_of_pages,
            pub_type="Magazine"
        )

        DigitalAsset.__init__(
            self,
            file_path=file_path
        )

        self._issn = issn
        self._issue_number = issue_number

    @property
    def issn(self):
        """Get the magazine's ISSN."""
        return self._issn
    
    @property
    def issue_number(self):
        """Get the magazine's issue number."""
        return self._issue_number

