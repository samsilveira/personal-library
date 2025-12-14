"""
Strategies package for different report generation algorithms.

This package implements the Strategy Pattern to allow flexible
report generation with different algorithms.
"""

from .report_strategy import ReportStrategy
from .evaluation_report import EvaluationReportStrategy
from .top_rated_report import TopRatedReportStrategy
from .progress_report import ProgressReportStrategy

__all__ = [
    'ReportStrategy',
    'EvaluationReportStrategy',
    'TopRatedReportStrategy',
    'ProgressReportStrategy'
]