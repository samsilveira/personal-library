"""
Module containing data persistinf functions.
"""

import sqlite3
from typing import List
from ..models import Publication, Annotation

def save_publication(conn: sqlite3.Connection, publication: Publication) -> bool:
    """
    Save a publication to the database.

    Args:
        conn: Datavase connection
        publication: Publication object to save

    Returns:
        True if saved sucessfully, False otherwise
    """
    pass

def load_publications(conn: sqlite3.Connection) -> List[Publication]:
    """
    Load all publications from the database.

    Args:
        conn: Database connection

    Returns:
        List of Publication object
    """
    pass

def update_publication(conn: sqlite3.Connection, publication: Publication) -> bool:
    """
    Update an existing publication in the database.

    Args:
        conn: Database connection
        publication: Publication object with updated data

    Returns:
        True if updated sucessfully, False otherwise
    """
    pass

def delete_publication(conn: sqlite3.Connection, publication_id: str) -> bool:
    """
    Delete a publication from the database.

    Args:
        conn: Database connection
        publication_id: ID of publication to delete

    Returns:
        True if deleted sucessfully, False otherwise
    """
    pass

def save_anntotation(conn: sqlite3.Connection, publication_id: str, annotation: Annotation) -> bool:
    """
    Save an annotation to the database.

    Args:
        conn: Database connection
        publication_id: ID of the associated publication
        annotation: Annotation object to save

    Returns:
        True if saved sucessfully, False otherwise
    """
    pass

def load_annotatios(conn: sqlite3.Connection, publication_id: str) -> List[Annotation]:
    """
    Load all annotations for a specific publication.

    Args:
        conn: Database connection
        publication_id: ID of the publication
    
    Returns:
        List of Annotation objects
    """
    pass