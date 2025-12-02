"""
Data persistence layer.

Manages system data storage and retrieval.
"""

from .repository import save_publication, load_publications

__all__ = [
    'save__publication',
    'load_publications',
]