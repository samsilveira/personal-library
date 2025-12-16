"""
Unit tests for EvaluationReport strategy.
"""

import pytest
from src.models import Collection, Book
from src.strategies import EvaluationReportStrategy as EvaluationReport


class TestEvaluationReport:
    """Test cases for EvaluationReport strategy."""
    
    def test_generate_evaluation_report(self, collection_with_ratings):
        """Test generating evaluation report."""
        strategy = EvaluationReport()
        publications = collection_with_ratings.list_publications()
        report_data = strategy.generate(publications)
        
        assert 'average' in report_data
        assert 'total_evaluated' in report_data
        assert 'total_publications' in report_data
        assert 'max_rating' in report_data
        assert 'min_rating' in report_data
        assert 'distribution' in report_data
        assert 'most_common' in report_data
        assert 'std_dev' in report_data
    
    def test_average_rating_calculation(self, collection_with_ratings):
        """Test that average rating is calculated correctly."""
        strategy = EvaluationReport()
        publications = collection_with_ratings.list_publications()
        report_data = strategy.generate(publications)
        
        expected_avg = (7.0 + 8.5 + 9.0 + 6.5 + 10.0) / 5
        
        assert report_data['average'] == pytest.approx(expected_avg, rel=1e-2)
        assert report_data['total_evaluated'] == 5
        assert report_data['total_publications'] == 5
    
    def test_highest_and_lowest_rated(self, collection_with_ratings):
        """Test identification of highest and lowest rated publications."""
        strategy = EvaluationReport()
        publications = collection_with_ratings.list_publications()
        report_data = strategy.generate(publications)
        
        assert report_data['max_rating'] == 10.0
        assert report_data['min_rating'] == 6.5
    
    def test_empty_collection(self, empty_collection):
        """Test report generation with empty collection."""
        strategy = EvaluationReport()
        publications = empty_collection.list_publications()
        report_data = strategy.generate(publications)
        
        assert report_data['average'] is None
        assert report_data['total_evaluated'] == 0
        assert report_data['total_publications'] == 0
        assert report_data['max_rating'] is None
        assert report_data['max_rating'] is None
        assert report_data['distribution'] == {}
        assert report_data['most_common'] is None
    
    def test_collection_with_no_ratings(self):
        """Test report with unrated publications."""
        collection = Collection()
        book1 = Book(1, "Unrated 1", "Autor", "Editora", 2025, "Ficção", 100)
        book2 = Book(2, "Unrated 2", "Autor", "Editora", 2025, "Ficção", 100)
        collection.register_publication(book1)
        collection.register_publication(book2)
        
        strategy = EvaluationReport()
        publications = collection.list_publications()
        report_data = strategy.generate(publications)
        
        assert report_data['average'] is None
        assert report_data['total_evaluated'] == 0
        assert report_data['total_publications'] == 2
        assert report_data['distribution'] == {}

    def test_standart_deviation_calculation(self, collection_with_ratings):
        """Test standard deviation calculation."""
        strategy = EvaluationReport()
        publications = collection_with_ratings.list_publications()
        report_data = strategy.generate(publications)

        assert report_data['std_dev'] > 0
        assert isinstance(report_data['std_dev'], float)
    
    def test_standart_deviation_single_rating(self):
        """Test standard deviation calculation."""
        collection = Collection()
        book = Book(1, "Livro", "Autor", "Editora", 2025, "Ficção", 100)
        book.start_reading()
        book.finish_reading()
        book.rate_publication(8.0)
        collection.register_publication(book)

        strategy = EvaluationReport()
        publications = collection.list_publications()
        report_data = strategy.generate(publications)

        assert report_data['std_dev'] == 0