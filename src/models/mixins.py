"""
Module containing mixin classes for shared functionality.
"""

from pathlib import Path

class DigitalAsset():
    """
    Mixin that adds digital file capabilities to a class.

    Provides file path management and validation for digital publications.

    Attributes:
        file_path (str): Path to the digital file.
    """

    def __init__(self, file_path: str = "", **kwargs):
        """
        Initialize digital asset capabilities.

        Args:
            file_path: Path to the digital file (optional)
            **kwargs: Additional arguments passed to other parent classes
        """

        super().__init__(**kwargs)
        self._file_path = file_path

    @property
    def file_path(self) -> str:
        """Get the file path."""
        return self._file_path
    
    def has_digital_file(self) -> bool:
        """
        Check if a digital file path is set.

        Returns:
            True if file_path is not empty, False otherwise
        """
        return bool(self.file_path and self.file_path.strip())

    def validate_file_exists(self) -> bool:
        """
        Validate if the actual file exists in the filesystem.

        Returns:
            True if file exists, False otherwise
        """
        return Path(self._file_path).exists()