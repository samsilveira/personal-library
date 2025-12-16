"""
Unit tests for TopRatedReportStrategy.
"""

import pytest
from src.models import Collection, Book, Magazine
from src.strategies.top_rated_report import TopRatedReportStrategy


class TestTopRatedReportStrategy:
    """Test cases for TopRatedReportStrategy."""
    
    def test_generate_top_rated_report(self, collection_with_ratings):
        """Test generating top rated report with default limit."""
        strategy = TopRatedReportStrategy()
        publications = collection_with_ratings.list_publications()
        report_data = strategy.generate(publications)
        
        assert 'limit' in report_data
        assert 'total_evaluated' in report_data
        assert 'top_publications' in report_data
        assert report_data['limit'] == 5  # default
        assert report_data['total_evaluated'] == 5
        assert len(report_data['top_publications']) == 5
    
    def test_top_publications_order(self, collection_with_ratings):
        """Test that publications are ordered by rating (descending)."""
        strategy = TopRatedReportStrategy()
        publications = collection_with_ratings.list_publications()
        report_data = strategy.generate(publications)
        
        top_pubs = report_data['top_publications']
        
        assert top_pubs[0]['rating'] == 10.0
        assert top_pubs[1]['rating'] == 9.0
        assert top_pubs[2]['rating'] == 8.5
        assert top_pubs[3]['rating'] == 7.0
        assert top_pubs[4]['rating'] == 6.5
        
        ratings = [pub['rating'] for pub in top_pubs]
        assert ratings == sorted(ratings, reverse=True)
    
    def test_top_n_limit(self, collection_with_ratings):
        """Test custom limit parameter."""
        strategy = TopRatedReportStrategy()
        publications = collection_with_ratings.list_publications()
        
        report_data = strategy.generate(publications, limit=3)
        assert report_data['limit'] == 3
        assert len(report_data['top_publications']) == 3
        
        report_data = strategy.generate(publications, limit=2)
        assert report_data['limit'] == 2
        assert len(report_data['top_publications']) == 2
    
    def test_empty_collection(self, empty_collection):
        """Test report generation with empty collection."""
        strategy = TopRatedReportStrategy()
        publications = empty_collection.list_publications()
        report_data = strategy.generate(publications)
        
        assert report_data['total_evaluated'] == 0
        assert report_data['top_publications'] == []
    
    def test_fewer_publications_than_limit(self):
        """Test when collection has fewer rated publications than limit."""
        collection = Collection()
        
        book1 = Book(1, "Book 1", "Author", "Pub", 2020, "Fiction", 100)
        book1.start_reading()
        book1.finish_reading()
        book1.rate_publication(8.0)
        
        book2 = Book(2, "Book 2", "Author", "Pub", 2021, "Fiction", 150)
        book2.start_reading()
        book2.finish_reading()
        book2.rate_publication(9.0)
        
        collection.register_publication(book1)
        collection.register_publication(book2)
        
        strategy = TopRatedReportStrategy()
        publications = collection.list_publications()
        report_data = strategy.generate(publications, limit=5)
        
        assert report_data['limit'] == 5
        assert len(report_data['top_publications']) == 2
        assert report_data['total_evaluated'] == 2
    
    def test_unrated_publications_excluded(self):
        """Test that unrated publications are not included."""
        collection = Collection()
        
        book1 = Book(1, "Rated 1", "Author", "Pub", 2020, "Fiction", 100)
        book1.start_reading()
        book1.finish_reading()
        book1.rate_publication(8.0)
        
        book2 = Book(2, "Rated 2", "Author", "Pub", 2021, "Fiction", 150)
        book2.start_reading()
        book2.finish_reading()
        book2.rate_publication(9.0)
        
        book3 = Book(3, "Unrated", "Author", "Pub", 2022, "Fiction", 200)
        book3.start_reading()
        book3.finish_reading()
        
        collection.register_publication(book1)
        collection.register_publication(book2)
        collection.register_publication(book3)
        
        strategy = TopRatedReportStrategy()
        publications = collection.list_publications()
        report_data = strategy.generate(publications, limit=5)
        
        assert report_data['total_evaluated'] == 2
        assert len(report_data['top_publications']) == 2
    
    def test_publication_details_structure(self, collection_with_ratings):
        """Test that each publication has the correct structure."""
        strategy = TopRatedReportStrategy()
        publications = collection_with_ratings.list_publications()
        report_data = strategy.generate(publications, limit=1)
        
        pub = report_data['top_publications'][0]
        
        assert 'id' in pub
        assert 'title' in pub
        assert 'author' in pub
        assert 'rating' in pub
        assert 'type' in pub
        assert 'year' in pub
        assert 'status' in pub
    
    def test_book_type_identification(self):
        """Test that books are correctly identified."""
        collection = Collection()
        book = Book(1, "Test Book", "Author", "Pub", 2020, "Fiction", 100)
        book.start_reading()
        book.finish_reading()
        book.rate_publication(8.0)
        collection.register_publication(book)
        
        strategy = TopRatedReportStrategy()
        publications = collection.list_publications()
        report_data = strategy.generate(publications)
        
        assert report_data['top_publications'][0]['type'] == 'Livro'
    
    def test_magazine_type_identification(self):
        """Test that magazines are correctly identified."""
        collection = Collection()
        magazine = Magazine(1, "Test Magazine", "Author", "Pub", 2020, "Science", 50, 
                           issue_number=1, issn="1234-5678")
        magazine.start_reading()
        magazine.finish_reading()
        magazine.rate_publication(9.0)
        collection.register_publication(magazine)
        
        strategy = TopRatedReportStrategy()
        publications = collection.list_publications()
        report_data = strategy.generate(publications)
        
        assert report_data['top_publications'][0]['type'] == 'Revista'
    
    def test_same_rating_sorted_by_title(self):
        """Test that publications with same rating are sorted alphabetically."""
        collection = Collection()
        
        titles = ["Zebra", "Alpha", "Mango"]
        for i, title in enumerate(titles, start=1):
            book = Book(i, title, "Author", "Pub", 2020, "Fiction", 100)
            book.start_reading()
            book.finish_reading()
            book.rate_publication(8.0)
            collection.register_publication(book)
        
        strategy = TopRatedReportStrategy()
        publications = collection.list_publications()
        report_data = strategy.generate(publications)
        
        top_pubs = report_data['top_publications']
        
        assert top_pubs[0]['title'] == "Alpha"
        assert top_pubs[1]['title'] == "Mango"
        assert top_pubs[2]['title'] == "Zebra"
    
    def test_format_output_with_data(self, collection_with_ratings):
        """Test output formatting with data."""
        strategy = TopRatedReportStrategy()
        publications = collection_with_ratings.list_publications()
        report_data = strategy.generate(publications, limit=3)
        
        formatted = strategy.format_output(report_data)
        
        assert "TOP 3 PUBLICAÇÕES" in formatted
        assert "🥇" in formatted
        assert "🥈" in formatted
        assert "🥉" in formatted
        assert "Autor:" in formatted
        assert "Nota:" in formatted
        assert "⭐" in formatted
        assert "Tipo:" in formatted
        assert "Status:" in formatted
    
    def test_format_output_empty(self, empty_collection):
        """Test output formatting with empty collection."""
        strategy = TopRatedReportStrategy()
        publications = empty_collection.list_publications()
        report_data = strategy.generate(publications, limit=5)
        
        formatted = strategy.format_output(report_data)
        
        assert "TOP 5 PUBLICAÇÕES" in formatted
        assert "Nenhuma publicação avaliada" in formatted
    
    def test_format_output_medals(self):
        """Test that medals are displayed correctly for top 3."""
        collection = Collection()
        
        for i in range(1, 6):
            book = Book(i, f"Book {i}", "Author", "Pub", 2020, "Fiction", 100)
            book.start_reading()
            book.finish_reading()
            book.rate_publication(10.0 - i)
            collection.register_publication(book)
        
        strategy = TopRatedReportStrategy()
        publications = collection.list_publications()
        report_data = strategy.generate(publications, limit=5)
        
        formatted = strategy.format_output(report_data)
        
        assert "🥇" in formatted
        assert "🥈" in formatted
        assert "🥉" in formatted
        assert "4." in formatted
        assert "5." in formatted
    
    def test_limit_zero(self, collection_with_ratings):
        """Test with limit=0."""
        strategy = TopRatedReportStrategy()
        publications = collection_with_ratings.list_publications()
        report_data = strategy.generate(publications, limit=0)
        
        assert report_data['limit'] == 0
        assert len(report_data['top_publications']) == 0
    
    def test_limit_exceeds_collection_size(self):
        """Test with limit larger than collection."""
        collection = Collection()
        
        for i in range(1, 4):
            book = Book(i, f"Book {i}", "Author", "Pub", 2020, "Fiction", 100)
            book.start_reading()
            book.finish_reading()
            book.rate_publication(float(i))
            collection.register_publication(book)
        
        strategy = TopRatedReportStrategy()
        publications = collection.list_publications()
        report_data = strategy.generate(publications, limit=10)
        
        assert len(report_data['top_publications']) == 3


class TestTopRatedReportEdgeCases:
    """Test edge cases for TopRatedReportStrategy."""
    
    def test_all_publications_same_rating(self):
        """Test when all publications have identical rating."""
        collection = Collection()
        
        titles = ["Zebra", "Alpha", "Mango", "Beta"]
        for i, title in enumerate(titles, start=1):
            book = Book(i, title, "Author", "Pub", 2020, "Fiction", 100)
            book.start_reading()
            book.finish_reading()
            book.rate_publication(7.5)
            collection.register_publication(book)
        
        strategy = TopRatedReportStrategy()
        publications = collection.list_publications()
        report_data = strategy.generate(publications, limit=3)
        
        top_pubs = report_data['top_publications']
        
        assert top_pubs[0]['title'] == "Alpha"
        assert top_pubs[1]['title'] == "Beta"
        assert top_pubs[2]['title'] == "Mango"
        assert all(pub['rating'] == 7.5 for pub in top_pubs)
    
    def test_mixed_books_and_magazines(self):
        """Test with both books and magazines."""
        collection = Collection()
        
        book = Book(1, "Great Book", "Author", "Pub", 2020, "Fiction", 300)
        book.start_reading()
        book.finish_reading()
        book.rate_publication(9.5)
        
        magazine = Magazine(2, "Amazing Magazine", "Editor", "Pub", 2021, "Science", 80,
                           issue_number=5, issn="1234-5678")
        magazine.start_reading()
        magazine.finish_reading()
        magazine.rate_publication(9.8)
        
        collection.register_publication(book)
        collection.register_publication(magazine)
        
        strategy = TopRatedReportStrategy()
        publications = collection.list_publications()
        report_data = strategy.generate(publications)
        
        top_pubs = report_data['top_publications']
        
        assert top_pubs[0]['title'] == "Amazing Magazine"
        assert top_pubs[0]['type'] == "Revista"
        assert top_pubs[0]['rating'] == 9.8
        
        assert top_pubs[1]['title'] == "Great Book"
        assert top_pubs[1]['type'] == "Livro"
        assert top_pubs[1]['rating'] == 9.5
    
    def test_status_field_present(self, collection_with_ratings):
        """Test that status field is included correctly."""
        strategy = TopRatedReportStrategy()
        publications = collection_with_ratings.list_publications()
        report_data = strategy.generate(publications, limit=1)
        
        pub = report_data['top_publications'][0]
        
        assert isinstance(pub['status'], str)
        assert pub['status'] in ['READ', 'READING', 'UNREAD']