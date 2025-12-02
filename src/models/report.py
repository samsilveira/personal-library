"""
Module containing the Report class.
"""

from typing import Dict, List, Tuple
from datetime import date
from .collection import Collection
from .publication import Publication
from .configuration import Configuration

class Report:
    """
    Stateless service class responsible for generating metrics and reports.

    Process data from a Collection to produce various statics about the user's reading habits and library composition.
    """

    @staticmethod
    def check_total_publications(collection: Collection) -> int:
        """
        Count total number of publications in the collection.

        Args:
            collection: Collection to analyze
        
        Returns:
            Total number of publications
        """
        return len(collection.list_publications())

    @staticmethod
    def check_publications_by_status(collection: Collection) -> Dict[str, Tuple[int, float]]:
        """
        Calculate quantity and percentage of publicatons by status.

        Args:
            collections: Collections to analyze

        Returns:
            Dictionary with status as key and tuple (count, percentage) as value
            Example: {"UNREAD": (7, 35.0), "READING": (3, 15.0), "READ": (10, 50.0)}
        """
        total = Report.check_total_publications(collection)
        statuses = ["UNREAD", "READING", "READ"]
        if total == 0:
            return {"UNREAD": (0, 0.0), "READING": (0, 0.0), "READ": (0, 0.0)}
        return {
            status: (
                count := len(collection.search_by_status(status)),
                (count / total * 100) if total > 0 else 0.0
            )
            for status in statuses
        }

    @staticmethod
    def calculate_average_rating(collection: Collection) -> float:
        """
        Calculate average rating of all read publications.

        Args:
            collection: Collection to analyze
        
        Returns:
            Average rating (0-10), or 0 if no rated publications exist
        """
        ratings = [pub.rating for pub in collection.search_by_status("READ") if pub.rating is not None]

        return sum(ratings) / len(ratings) if ratings else 0.0

    @staticmethod
    def check_top_5_publications(collection: Collection) -> List[Publication]:
        """
        Get the top 5 highest-rated publications.

        Args:
            collection: Collection to analyze

        Returns:
            List of up to 5 publications sorted by rating (highest first)
        """
        return sorted([pub for pub in collection.search_by_status("READ") if pub.rating is not None],
                         key=lambda pub : pub.rating,
                         reverse=True)[:5]

    @staticmethod
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