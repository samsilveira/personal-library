"""
Models package containing all domain classes.
"""

from .user import User
from .collection import Collection
from .configuration import Configuration
from .publication import Publication, Book, Magazine
from .mixins import DigitalAsset
from .annotation import Annotation
from .report import Report

__all__ = [
    'User',
    'Collection',
    'Configuration',
    'DigitalAsset',
    'Publication',
    'Book',
    'Magazine',
    'Annotation',
    'Report'
]