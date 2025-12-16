"""
Unit tests for Report class.
"""

import pytest
from datetime import date
from src.models import Report, Collection, Book, Magazine, Configuration

class TestReportExistingMethods:
    """Tests for existing Report methods."""
    
    def test_check_total_publications_empty(self, empty_collection):
        """Test total count with empty collection."""
        assert Report.check_total_publications(empty_collection) == 0
    
    def test_check_total_publications_populated(self, populated_collection):
        """Test total count with populated collection."""
        assert Report.check_total_publications(populated_collection) == 5
    
    def test_check_publications_by_status_empty(self, empty_collection):
        """Test status distribution with empty collection."""
        result = Report.check_publications_by_status(empty_collection)
        
        assert result["UNREAD"] == (0, 0.0)
        assert result["READING"] == (0, 0.0)
        assert result["READ"] == (0, 0.0)
    
    def test_check_publications_by_status_populated(self, populated_collection):
        """Test status distribution with populated collection."""
        result = Report.check_publications_by_status(populated_collection)
        
        assert result["UNREAD"] == (2, 40.0)
        assert result["READING"] == (1, 20.0)
        assert result["READ"] == (2, 40.0)
    
    def test_check_publications_by_status_all_unread(self):
        """Test status distribution when all publications are unread."""
        collection = Collection()
        for i in range(1, 4):
            book = Book(i, f"Book {i}", "Author", "Pub", 2020, "Fiction", 200)
            collection.register_publication(book)
        
        result = Report.check_publications_by_status(collection)
        
        assert result["UNREAD"] == (3, 100.0)
        assert result["READING"] == (0, 0.0)
        assert result["READ"] == (0, 0.0)
    
    def test_calculate_average_rating_no_ratings(self, empty_collection):
        """Test average rating with no rated books."""
        assert Report.calculate_average_rating(empty_collection) == 0.0
    
    def test_calculate_average_rating_with_ratings(self, populated_collection):
        """Test average rating calculation."""
        assert Report.calculate_average_rating(populated_collection) == 8.75
    
    def test_calculate_average_rating_ignores_unrated(self):
        """Test that unrated books don't affect average."""
        collection = Collection()
        
        book1 = Book(1, "Rated", "Author", "Pub", 2020, "Fiction", 200)
        book1.start_reading()
        book1.finish_reading()
        book1.rate_publication(10.0)
        
        book2 = Book(2, "Unrated", "Author", "Pub", 2021, "Fiction", 200)
        book2.start_reading()
        book2.finish_reading()
        
        collection.register_publication(book1)
        collection.register_publication(book2)
        
        assert Report.calculate_average_rating(collection) == 10.0
    
    def test_check_top_5_publications_empty(self, empty_collection):
        """Test top 5 with no books."""
        assert Report.check_top_5_publications(empty_collection) == []
    
    def test_check_top_5_publications(self, populated_collection):
        """Test top 5 retrieval."""
        top = Report.check_top_5_publications(populated_collection)
        
        assert len(top) == 2
        assert top[0].rating == 9.0
        assert top[1].rating == 8.5
    
    def test_check_top_5_publications_more_than_5(self):
        """Test top 5 when there are more than 5 rated books."""
        collection = Collection()
        
        ratings = [9.5, 8.0, 10.0, 7.5, 9.0, 8.5, 6.0]
        for i, rating in enumerate(ratings, start=1):
            book = Book(i, f"Book {i}", "Author", "Pub", 2020, "Fiction", 200)
            book.start_reading()
            book.finish_reading()
            book.rate_publication(rating)
            collection.register_publication(book)
        
        top = Report.check_top_5_publications(collection)
        
        assert len(top) == 5
        assert top[0].rating == 10.0
        assert top[1].rating == 9.5
        assert top[2].rating == 9.0
        assert top[3].rating == 8.5
        assert top[4].rating == 8.0
    
    def test_check_annual_goal_progress(self, collection_for_annual_goal, sample_configuration):
        """Test annual goal progress calculation."""
        result = Report.check_annual_goal_progress(collection_for_annual_goal, sample_configuration)
        
        assert result["goal"] == 12
        assert result["completed"] == 3
        assert result["remaining"] == 9
        assert result["percentage"] == 25.0
        assert "on_track" in result
        assert "expected_progress" in result
    
    def test_check_annual_goal_progress_exceeds_goal(self, sample_configuration):
        """Test when books read exceeds annual goal."""
        collection = Collection()
        current_year = date.today().year
        
        for i in range(1, 16):
            book = Book(i, f"Book {i}", "Author", "Pub", current_year, "Fiction", 200)
            book.start_reading()
            book.finish_reading()
            collection.register_publication(book)
        
        result = Report.check_annual_goal_progress(collection, sample_configuration)
        
        assert result["goal"] == 12
        assert result["completed"] == 15
        assert result["remaining"] == 0
        assert result["percentage"] == 125.0


class TestReportNewMethods:
    """Tests for new visualization methods."""
    
    def test_generate_status_report_dict_structure(self, populated_collection):
        """Test dictionary report structure."""
        result = Report.generate_status_report_dict(populated_collection)
        
        assert "total_publications" in result
        assert "by_status" in result
        assert "generated_at" in result
        
        assert "unread" in result["by_status"]
        assert "reading" in result["by_status"]
        assert "read" in result["by_status"]
    
    def test_generate_status_report_dict_values(self, populated_collection):
        """Test dictionary report values."""
        result = Report.generate_status_report_dict(populated_collection)
        
        assert result["total_publications"] == 5
        assert result["by_status"]["unread"]["count"] == 2
        assert result["by_status"]["unread"]["percentage"] == 40.0
        assert result["by_status"]["reading"]["count"] == 1
        assert result["by_status"]["reading"]["percentage"] == 20.0
        assert result["by_status"]["read"]["count"] == 2
        assert result["by_status"]["read"]["percentage"] == 40.0
    
    def test_generate_status_report_dict_empty(self, empty_collection):
        """Test dictionary report with empty collection."""
        result = Report.generate_status_report_dict(empty_collection)
        
        assert result["total_publications"] == 0
        assert result["by_status"]["unread"]["count"] == 0
        assert result["by_status"]["reading"]["count"] == 0
        assert result["by_status"]["read"]["count"] == 0
    
    def test_generate_status_report_dict_date_format(self, populated_collection):
        """Test that generated_at is in ISO format."""
        result = Report.generate_status_report_dict(populated_collection)
        
        assert result["generated_at"] == date.today().isoformat()
    
    def test_print_status_report_empty(self, empty_collection, capsys):
        """Test console output with empty collection."""
        Report.print_status_report(empty_collection)
        
        captured = capsys.readouterr()
        assert "Nenhuma publicação cadastrada" in captured.out
        assert "Total de Publicações: 0" in captured.out
    
    def test_print_status_report_populated(self, populated_collection, capsys):
        """Test console output with populated collection."""
        Report.print_status_report(populated_collection)
        
        captured = capsys.readouterr()
        assert "Total de Publicações: 5" in captured.out
        assert "Não Lidos" in captured.out
        assert "Lendo" in captured.out
        assert "Lidos" in captured.out
        assert "40.0%" in captured.out
        assert "20.0%" in captured.out
    
    def test_print_status_report_has_progress_bars(self, populated_collection, capsys):
        """Test that progress bars are displayed."""
        Report.print_status_report(populated_collection)
        
        captured = capsys.readouterr()
        assert "█" in captured.out
        assert "░" in captured.out
    
    def test_print_full_report_with_ratings(self, populated_collection, capsys):
        """Test full report output."""
        Report.print_full_report(populated_collection)
        
        captured = capsys.readouterr()
        assert "RELATÓRIO COMPLETO" in captured.out
        assert "ESTATÍSTICAS GERAIS" in captured.out
        assert "DISTRIBUIÇÃO POR STATUS" in captured.out
        assert "TOP 5 PUBLICAÇÕES" in captured.out
        assert "8.75" in captured.out
    
    def test_print_full_report_empty(self, empty_collection, capsys):
        """Test full report with empty collection."""
        Report.print_full_report(empty_collection)
        
        captured = capsys.readouterr()
        assert "RELATÓRIO COMPLETO" in captured.out
        assert "Total de Publicações: 0" in captured.out
    
    def test_print_full_report_shows_top_5(self, capsys):
        """Test that full report shows top 5 publications."""
        collection = Collection()
        
        ratings = [9.5, 8.0, 10.0, 7.5, 9.0]
        for i, rating in enumerate(ratings, start=1):
            book = Book(i, f"Top Book {i}", "Author", "Pub", 2020, "Fiction", 200)
            book.start_reading()
            book.finish_reading()
            book.rate_publication(rating)
            collection.register_publication(book)
        
        Report.print_full_report(collection)
        
        captured = capsys.readouterr()
        assert "TOP 5 PUBLICAÇÕES" in captured.out
        assert "10.0/10" in captured.out
        assert "9.5/10" in captured.out
        assert "✦" in captured.out
    
    def test_print_full_report_no_top_5_when_no_ratings(self, capsys):
        """Test that TOP 5 section doesn't appear when no ratings exist."""
        collection = Collection()
        book = Book(1, "Unrated", "Author", "Pub", 2020, "Fiction", 200)
        collection.register_publication(book)
        
        Report.print_full_report(collection)
        
        captured = capsys.readouterr()
        assert "TOP 5 PUBLICAÇÕES" not in captured.out

class TestReportEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_report_with_only_magazines(self):
        """Test that reports work with magazines too."""
        collection = Collection()
        
        mag1 = Magazine(1, "Magazine 1", "Editor", "Pub", 2024, "Tech", 100, 12)
        mag1.start_reading()
        mag1.finish_reading()
        mag1.rate_publication(7.5)
        
        collection.register_publication(mag1)
        
        assert Report.check_total_publications(collection) == 1
        assert Report.calculate_average_rating(collection) == 7.5
    
    def test_report_with_mixed_publications(self):
        """Test reports with both books and magazines."""
        collection = Collection()
        
        book = Book(1, "Book", "Author", "Pub", 2020, "Fiction", 300)
        mag = Magazine(2, "Magazine", "Editor", "Pub", 2024, "Tech", 100, 12)
        
        collection.register_publication(book)
        collection.register_publication(mag)
        
        assert Report.check_total_publications(collection) == 2
    
    def test_percentage_rounding_in_dict(self):
        """Test that percentages are properly rounded in dict report."""
        collection = Collection()
        
        book1 = Book(1, "Read", "Author", "Pub", 2020, "Fiction", 200)
        book1.start_reading()
        book1.finish_reading()
        
        book2 = Book(2, "Unread 1", "Author", "Pub", 2020, "Fiction", 200)
        book3 = Book(3, "Unread 2", "Author", "Pub", 2020, "Fiction", 200)
        
        collection.register_publication(book1)
        collection.register_publication(book2)
        collection.register_publication(book3)
        
        result = Report.generate_status_report_dict(collection)
        
        assert result["by_status"]["read"]["percentage"] == 33.33
        assert result["by_status"]["unread"]["percentage"] == 66.67