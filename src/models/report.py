"""
Module containing the Report class.
"""

from typing import Dict, List, Tuple
from .collection import Collection
from .publication import Publication
from .configuration import Configuration

class Report:
    """
    Stateless service class responsible for generating metrics and reports.

    Process data from a Collection to produce various statics about the user's reading habits and library composition.
    """

    def check_total_publications(collection: Collection) -> int:
        """
        Count total number of publications in the collection.

        Args:
            collection: Collection to analyze
        
        Returns:
            Total number of publications
        """
        pass

    def check_publications_by_status(collection: Collection) -> Dict[str, Tuple[int, float]]:
        """
        Calculate quantity and percentage of publicatons by status.

        Args:
            collections: Collections to analyze

        Returns:
            Dictionary with status as key and tuple (count, percentage) as value
            Example: {"READ": (10, 50.0), "READING": (3, 15.0), "NOT_READ": (7, 35.0)}
        """
        pass

    def calculate_average_ratings(collection: Collection) -> float:
        """
        Calculate average rating of all read publications.

        Args:
            collection: Collection to analyze
        
        Returns:
            Average rating (0-10), or 0 if no rated publications exist
        """
        pass

    def check_top_5_publications(collection: Collection) -> List[Publication]:
        """
        Get the top 5 highest-rated publications.

        Args:
            collection: Collection to analyze

        Returns:
            List of up to 5 publications sorted by rating (highest first)
        """
        pass

    def check_annual_goal_progress(collection: Collection, configuration: Configuration) -> Dict[str, any]:
        """
        Check progress towards annual reading goal.

        Args:
            collection: Collection to analyze
            configuration: Configuration with annual goal

        Returns:
            Dictionary with keys:
            - 'goal': targer number
            - 'completed': books read this year
            - 'remaining': books still needed
            - 'percentage': progress percentage
            - 'on_track': boolena indicating if on pace
        """
        pass