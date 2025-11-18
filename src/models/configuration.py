"""
Module containing the Configuration class.
"""

class Configuration:
    """
    Stores user preferences and goals for the library;

    Handles loading and saving settings from/to settings.json file.

    Attributes:
        annual_goal (int): Target number of books to read per year
        simultaneous_reading_limit (int): Maximum number of books being read at once
		favorite_genre (str): User's preferred literary genre
    """

    def __init__(self, annual_goal: int = 15, simultaneous_reading__limit: int = 3, favorite_genre: str = "Fiction"):
        """
        Initialize configuration with default or provided values.

        Args:
            annual_goal: Yearly reading goal (default: 15)
            simultaneous_reading_limit: Max simultaneous readings (default: 3)
            favorite_genre: Preferred genre
        """
        pass

    def load_settings(self, filepath: str = "settings.json") -> None:
        """
        Load configuration from a JSON file.

        Args:
            filepath: Path to the settings file

        Raises:
            FileNotFoundErros: If settings file doesn't exist
            ValueErros: If settings file contains invalid data
        """
        pass

    def save_settings(self, filepath: str = "settings.json") -> None:
        """
        Save current configuration to a JSON file.

        Args:
            filepath: Path where the settings will be saved
        """
        pass
