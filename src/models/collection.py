"""
Module containing the Collection class.
"""

from datetime import date
from typing import Dict, List, Optional
from .publication import Publication
from .configuration import Configuration

class Collection:
    """
    Manages the complete set of publications in the user's library.

    Responsible for adding, removing, searching publications and enforcing business rules related to the collection as a whole.

    Attributes:
        publications (Dict[int, Publication]): Dictionary of publications indexed by ID
    """

    def __init__(self):
        """
        Initialize an empty collection.
        """
        self._publications = {}

    def register_publication(self, publication: Publication) -> bool:
        """
        Register a new publication in the collection.

        Validates that the publication doesn't already exist (same title and author).

        Args:
            publication: Publication object to be added

        Returns:
            True if sucessfully registerd, False otherwise

        Raises:
            TypeError: If publication is not a Publication object
            ValueError: If publication with same title and author already exists
        """
        if not isinstance(publication, Publication):
            raise TypeError("Must provide a Publication instance")

        if publication.id in self._publications:
            raise ValueError(f"Publication with ID {publication.id} already exists.")
        
        for existing_pub in self._publications.values():
            if existing_pub == publication:
                raise ValueError("Publication with same title and author already exists.")
            
        self._publications[publication.id] = publication
        return True

    def list_publications(self) -> list[Publication]:
        """
        Returns all publications in the collection.

        Returns:
            List of all Publication objects
        """
        return list(self._publications.values())

    def remove_publication(self, publication_id: int) -> bool:
        """
        Remove a publication from the collection.

        Args:
            publication_id: ID of the publication to remove

        Returns:
            True if sucessfully remove, False if not found 
        """
        if publication_id in self._publications:
            del self._publications[publication_id]
            return True
        return False

    def search_by_author(self, author: str) -> List[Publication]:
        """
        Search publication by author name.

        Args:
            author: Author name to search for

        Returns:
            List of publications by the specified author
        """
        return [pub for pub in self._publications.values() if author.lower() in pub.author.lower()]
              
    def search_by_title(self, title: str) -> List[Publication]:
        """
        Search publication by title.

        Args:
            title: Title to search for

        Returns:
            List of publications matching the title
        """
        return [pub for pub in self._publications.values() if title.lower() in pub.title.lower()]
        pass

    def search_by_status(self, status: str) -> List[Publication]:
        """
        Search publication by reading status.

        Args:
            status: Status to filter by (UNREAD, READING, READ)

        Returns:
            List of publications with the specified status
        """
        return [pub for pub in self._publications.values() if status.upper() == pub.status]
        pass

    def filter_by_reading_period(self, start_date: date, end_date: date) -> List[Publication]:
        """
        Filter publications by reading period.

        Args:
            start_date: Beginning of the period
            end_date: End of the period

        Returns:
            List of publications read during the specified period
        """
        return [pub for pub in self._publications.values() if pub.status == "READ" and start_date <= pub.end_read_date <= end_date]


    def start_publication_reading(self, publication_id: int, configuration: Configuration) -> bool:
        """
        Start reading a publication.

        Validates the simultaneous reading limit before allowing the operation.

        Args:
            publication_id: ID of the publication to start reading
            configuration: Configuration object with reading limits

        Returns:
            True if reading started sucessfully, False otherwise

        Raises:
            ValueError: If publication not found or simultaneous reading limit is reached
        """

        # 1. Encontrar a publicação pelo ID
        if publication_id not in self._publications:
            raise ValueError(f"Publication with ID {publication_id} not found.")
        
        simultaneous_reading = len(self.search_by_status("READING"))

        if simultaneous_reading >= configuration.simultaneous_reading_limit:
            raise ValueError("Maximum number of simultaneous readings reached.")
        
        self._publications[publication_id].start_reading()
        
        return True
        

    