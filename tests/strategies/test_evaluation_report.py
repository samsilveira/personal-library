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

    def test_most_common_rating(self):
        """Test identification of most common rating."""
        collection = Collection()
        
        for i in range(1, 4):
            book = Book(i, f"Livro {i}", "Autor", "Editora", 2025, "Ficção", 100)
            book.start_reading()
            book.finish_reading()
            book.rate_publication(8.0)
            collection.register_publication(book)
        
        for i in range(4, 6):
            book = Book(i, f"Livro {i}", "Autor", "Editora", 2025, "Ficção", 100)
            book.start_reading()
            book.finish_reading()
            book.rate_publication(9.0)
            collection.register_publication(book)
        
        strategy = EvaluationReport()
        publications = collection.list_publications()
        report_data = strategy.generate(publications)
        
        most_common_rating, count = report_data['most_common']
        assert most_common_rating == 8.0
        assert count == 3
    
    def test_distribution_format(self, collection_with_ratings):
        """Test that distribution is properly formatted."""
        strategy = EvaluationReport()
        publications = collection_with_ratings.list_publications()
        report_data = strategy.generate(publications)
        
        distribution = report_data['distribution']
        
        assert isinstance(distribution, dict)
        assert len(distribution) == 5
        assert all(count == 1 for count in distribution.values())
    
    def test_format_output_with_data(self, collection_with_ratings):
        """Test output formatting with data."""
        strategy = EvaluationReport()
        publications = collection_with_ratings.list_publications()
        report_data = strategy.generate(publications)
        
        formatted = strategy.format_output(report_data)
        
        assert "RELATÓRIO DE AVALIAÇÕES" in formatted
        assert "Média geral:" in formatted
        assert "Desvio padrão:" in formatted
        assert "Menor nota:" in formatted
        assert "Maior nota:" in formatted
        assert "Nota mais comum:" in formatted
        assert "Distribuição de notas:" in formatted
    
    def test_format_output_empty(self, empty_collection):
        """Test output formatting with empty collection."""
        strategy = EvaluationReport()
        publications = empty_collection.list_publications()
        report_data = strategy.generate(publications)
        
        formatted = strategy.format_output(report_data)
        
        assert "RELATÓRIO DE AVALIAÇÕES" in formatted
        assert "Nenhuma publicação avaliada" in formatted
    
    def test_mixed_rated_and_unrated(self):
        """Test with mix of rated and unrated publications."""
        collection = Collection()
        
        book1 = Book(1, "Avaliado 1", "Autor", "Editora", 2020, "Ficção", 100)
        book1.start_reading()
        book1.finish_reading()
        book1.rate_publication(8.0)
        
        book2 = Book(2, "Avaliado 2", "Autor", "Editora", 2021, "Ficção", 150)
        book2.start_reading()
        book2.finish_reading()
        book2.rate_publication(9.0)
        
        book3 = Book(3, "Não avaliado", "Autor", "Editora", 2022, "Ficção", 200)
        book3.start_reading()
        book3.finish_reading()
        
        collection.register_publication(book1)
        collection.register_publication(book2)
        collection.register_publication(book3)
        
        strategy = EvaluationReport()
        publications = collection.list_publications()
        report_data = strategy.generate(publications)
        
        assert report_data['total_publications'] == 3
        assert report_data['total_evaluated'] == 2
        assert report_data['average'] == 8.5


class TestEvaluationReportEdgeCases:
    """Test edge cases for EvaluationReportStrategy."""
    
    def test_all_same_rating(self):
        """Test when all publications have the same rating."""
        collection = Collection()
        
        for i in range(1, 4):
            book = Book(i, f"Livro {i}", "Autor", "Editora", 2020, "Ficção", 100)
            book.start_reading()
            book.finish_reading()
            book.rate_publication(7.5)
            collection.register_publication(book)
        
        strategy = EvaluationReport()
        publications = collection.list_publications()
        report_data = strategy.generate(publications)
        
        assert report_data['average'] == 7.5
        assert report_data['std_dev'] == 0.0
        assert report_data['min_rating'] == 7.5
        assert report_data['max_rating'] == 7.5
        assert report_data['most_common'] == (7.5, 3)
    
    def test_extreme_ratings(self):
        """Test with extreme ratings (0 and 10)."""
        collection = Collection()
        
        book1 = Book(1, "Pior", "Autor", "Editora", 2020, "Ficção", 100)
        book1.start_reading()
        book1.finish_reading()
        book1.rate_publication(0.0)
        
        book2 = Book(2, "Mehlor", "Autor", "Editora", 2021, "Ficção", 150)
        book2.start_reading()
        book2.finish_reading()
        book2.rate_publication(10.0)
        
        collection.register_publication(book1)
        collection.register_publication(book2)
        
        strategy = EvaluationReport()
        publications = collection.list_publications()
        report_data = strategy.generate(publications)
        
        assert report_data['average'] == 5.0
        assert report_data['min_rating'] == 0.0
        assert report_data['max_rating'] == 10.0
    
    def test_distribution_order(self):
        """Test that distribution is ordered by rating."""
        collection = Collection()
        
        ratings = [9.0, 6.0, 8.0, 7.0, 10.0]
        for i, rating in enumerate(ratings, start=1):
            book = Book(i, f"Livro {i}", "Autor", "Editora", 2020, "Ficção", 100)
            book.start_reading()
            book.finish_reading()
            book.rate_publication(rating)
            collection.register_publication(book)
        
        strategy = EvaluationReport()
        publications = collection.list_publications()
        report_data = strategy.generate(publications)
        
        distribution_keys = list(report_data['distribution'].keys())
        
        assert distribution_keys == sorted(distribution_keys)
        assert distribution_keys == [6.0, 7.0, 8.0, 9.0, 10.0]