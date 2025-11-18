"""
Models package containing all domain class.
"""

from .user import User
from .collection import Collection
from .configuration import Configuration
from .Publication import Publication, Book, Magazine
from .annotation import Annotation
from .report import Report

__all__ = [
    'User',
    'Collection',
    'Configuration',
    'Publication',
    'Book',
    'Magazine',
    'Annotation',
    'Report'
]