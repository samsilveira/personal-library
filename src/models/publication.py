"""
Module containing the Publication class and its specializations.
"""

from datetime import date
from abc import ABC

class Publication(ABC):
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

    def __init__(self, 
        pub_id: int, 
        title: str, 
        author: str, 
        publisher: str, 
        year: int, 
        genre: str, 
        number_of_pages: int,
        pub_type: str,
        file_path: str = ""
    ):
        """Initializes a new publication."""
        if not isinstance(pub_id, int) or pub_id <= 0:
            raise ValueError("ID must be a positive integer")
        self.__id = pub_id

        self._title = None
        self.title = title       
        
        self._year = None
        self.year = year
        
        self._author = author
        self._publisher = publisher
        self._genre = genre
        self._number_of_pages = number_of_pages
        self._pub_type = pub_type
        self._file_path = file_path
        
        self.__status = "UNREAD"
        self._start_read_date = None
        self._end_read_date = None
        self.__rating = None
        self._rating_inclusion_date = None
        self._annotations = []

    def __str__(self):
        return f"[{self.id}] {self.title} - {self._author}"
    
    def __repr__(self):
        return f"Publication(id={self.id}, title='{self.title}', year={self.year}, author='{self.author}', status='{self.status}')"
    
    def __eq__(self, other):
        if not isinstance(other, Publication):
            return False
        return self.title == other.title and self.author == other.author
    
    def __lt__(self, other):
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
            raise ValueError("Year must be greater then or equal to 1500")
        
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

    def start_reading(self):
        """
        Starts reading the publication.
        
        Updates the status to READING and registers the start date.
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

    def rate_publication(self, rating_value: float):
        """
        Registers a rating for the publication.

        Args:
            rating: Value between 0 and 10

        Raises:
            ValueError: If status is not READ or rating is invalid.
        """
        if not isinstance(rating_value, (int, float)):
            raise TypeError("The evaluation must of int or float type")
        
        if self.__status != "READ":
            raise ValueError("Publication cannot be evaluated without finishing reading")
        
        if 0 > rating_value or rating_value > 10:
            raise ValueError("The rating cannot be less than 0 or greater than 10")

        self.__rating = rating_value
        self._rating_inclusion_date = date.today()

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
        file_path="", 
        isbn="",
        edition=1
    ):
        """Initializes a new book."""
        super().__init__(
            pub_id=pub_id, 
            title=title, 
            author=author, 
            publisher=publisher, 
            year=year, 
            genre=genre,
            number_of_pages=number_of_pages,
            pub_type="Book",
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
        return f"[{self.id}] {self.title} - {self._author} (ISBN: {self.isbn})"

class Magazine(Publication):
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
        file_path="", 
        issn=""
    ):
        """Initializes a new magazine."""
        super().__init__(
            pub_id=pub_id,
            title=title,
            author=author,
            publisher=publisher,
            year=year,
            genre=genre,
            number_of_pages=number_of_pages,
            pub_type="Magazine",
            file_path=file_path
        )

        self._issn = issn
        self._issue_number = issue_number

    @property
    def issn(self):
        return self._issn
    
    @property
    def issue_number(self):
        return self._issue_number

