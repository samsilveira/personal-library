"""
Abstract Strategy for Report Generation
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from src.models import Publication


class ReportStrategy(ABC):
    """
    Abstract base class for different report generation strategies.
    
    This implements the Strategy Pattern, allowing different algorithms
    for generating reports to be selected at runtime.
    """
    
    @abstractmethod
    def generate(self, publications: List[Publication], **kwargs) -> Dict[str, Any]:
        """
        Generate a report based on the given publications.
        
        Args:
            publications: List of publications to analyze
            **kwargs: Additional parameters specific to each strategy
            
        Returns:
            Dictionary containing the report data
        """
        pass
    
    @abstractmethod
    def format_output(self, report_data: Dict[str, Any]) -> str:
        """
        Format the report data for display.
        
        Args:
            report_data: Dictionary containing report data
            
        Returns:
            Formatted string ready for display
        """
        pass