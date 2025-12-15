"""
Module containing the Configuration class.
"""

from pathlib import Path
import json

class Configuration:
    """
    Stores user preferences and goals for the library.

    Handles loading and saving settings from/to settings.json file.

    Attributes:
        annual_goal (int): Target number of books to read per year
        simultaneous_reading_limit (int): Maximum number of books being read at once
		favorite_genre (str): User's preferred literary genre
    """

    def __init__(self, 
        annual_goal: int = 15, 
        simultaneous_reading_limit: int = 3, 
        favorite_genre: str = "Fiction"
    ):
        """
        Initialize configuration with default or provided values.

        Args:
            annual_goal: Yearly reading goal (default: 15)
            simultaneous_reading_limit: Max simultaneous readings (default: 3)
            favorite_genre: Preferred genre
        """
        if annual_goal <= 0:
            raise ValueError("Annual target cannot be less than or equal to zero.")
        if simultaneous_reading_limit <= 0:
            raise ValueError("Limit for simultaneous readings cannot be less than or equal to zero.")
        
        self.annual_goal = annual_goal
        self.simultaneous_reading_limit = simultaneous_reading_limit
        self.favorite_genre = favorite_genre

    @property
    def annual_goal(self):
        return self._annual_goal
    
    @annual_goal.setter
    def annual_goal(self, value: int):
        if value <= 0:
            raise ValueError("Annual target cannot be less than or equal to zero.")
        self._annual_goal = value

    @property
    def simultaneous_reading_limit(self):
        return self._simultaneous_reading_limit
    
    @simultaneous_reading_limit.setter
    def simultaneous_reading_limit(self, value: int):
        if value <= 0:
            raise ValueError("Limit for simultaneous readings cannot be less than or equal to zero.")
        self._simultaneous_reading_limit = value

    def _to_dict(self) -> dict:
        """Convert configuration to dictionary for JSON serialization."""
        return {
                "annual_goal": self.annual_goal,
                "simultaneous_reading_limit": self.simultaneous_reading_limit,
                "favorite_genre": self.favorite_genre
            }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Configuration':
        """
        Create Configuration from dictionary.
        """
        configuration = cls(
            annual_goal=data["annual_goal"],
            simultaneous_reading_limit=data["simultaneous_reading_limit"],
            favorite_genre=data["favorite_genre"]
        )
        
        return configuration
        
    def load_settings(self, filepath: str = "settings.json") -> None:
        """
        Load configuration from a JSON file.

        Args:
            filepath: Path to the settings file

        Raises:
            FileNotFoundError: If settings file doesn't exist
            ValueError: If settings file contains invalid data
        """
        try:
            
            settings_data = self._to_dict()
            directory = (Path(__file__).parent.parent.parent / filepath).resolve()

            if not directory.exists():
                with open(directory, "w", encoding="utf-8") as file:
                    json.dump(settings_data, file, indent=4, ensure_ascii=False)

            with open(directory, "r", encoding="utf-8") as file:
                data = json.load(file)
        
            self.annual_goal = data.get("annual_goal", self.annual_goal)
            self.simultaneous_reading_limit = data.get("simultaneous_reading_limit", self.simultaneous_reading_limit)
            self.favorite_genre = data.get("favorite_genre", self.favorite_genre)

        except json.JSONDecodeError as e:
            print(f"Invalid JSON in {filepath}. Using default values.") 
        
    def save_settings(self, filepath: str = "settings.json") -> None:
        """
        Save current configuration to a JSON file.

        Args:
            filepath: Path where the settings will be saved
        """
        try:
            settings_data = self._to_dict()
            directory = (Path(__file__).parent.parent.parent / filepath).resolve()

            with open(directory, "w", encoding="utf-8") as file:
                json.dump(settings_data, file, indent=4, ensure_ascii=False)
        except Exception as e:
            raise IOError(f"Failed to save settings to {directory}: {e}")
        
