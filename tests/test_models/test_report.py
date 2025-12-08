import pytest
from models import Report
from io import StringIO
import sys

# Fixtures



# Testes dos métodos existentes
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
        
        # 2 UNREAD de 5 = 40%
        assert result["UNREAD"] == (2, 40.0)
        # 1 READING de 5 = 20%
        assert result["READING"] == (1, 20.0)
        # 2 READ de 5 = 40%
        assert result["READ"] == (2, 40.0)
    
    def test_calculate_average_rating_no_ratings(self, empty_collection):
        """Test average rating with no rated books."""
        assert Report.calculate_average_rating(empty_collection) == 0.0
    
    def test_calculate_average_rating_with_ratings(self, populated_collection):
        """Test average rating calculation."""
        # (8.5 + 9.0) / 2 = 8.75
        assert Report.calculate_average_rating(populated_collection) == 8.75
    
    def test_check_top_5_publications_empty(self, empty_collection):
        """Test top 5 with no books."""
        assert Report.check_top_5_publications(empty_collection) == []
    
    def test_check_top_5_publications(self, populated_collection):
        """Test top 5 retrieval."""
        top = Report.check_top_5_publications(populated_collection)
        
        assert len(top) == 2  # Só 2 livros têm rating
        assert top[0].rating == 9.0  # Maior rating primeiro
        assert top[1].rating == 8.5


# Testes dos novos métodos
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
    
    def test_print_status_report_empty(self, empty_collection, capsys):
        """Test console output with empty collection."""
        Report.print_status_report(empty_collection)
        
        captured = capsys.readouterr()
        assert "Nenhuma publicação cadastrada" in captured.out  # ✅ Corrigido typo
        assert "Total de Publicações: 0" in captured.out
    
    def test_print_status_report_populated(self, populated_collection, capsys):
        """Test console output with populated collection."""
        Report.print_status_report(populated_collection)
        
        captured = capsys.readouterr()
        assert "Total de Publicações: 5" in captured.out
        assert "Não Lidos" in captured.out
        assert "Lendo" in captured.out
        assert "Lidos" in captured.out
        assert "40.0%" in captured.out  # Aparece 2x (UNREAD e READ)
        assert "20.0%" in captured.out  # READING
    
    def test_print_full_report_with_ratings(self, populated_collection, capsys):
        """Test full report output."""
        Report.print_full_report(populated_collection)
        
        captured = capsys.readouterr()
        assert "RELATÓRIO COMPLETO" in captured.out
        assert "ESTATÍSTICAS GERAIS" in captured.out
        assert "DISTRIBUIÇÃO POR STATUS" in captured.out
        assert "TOP 5 PUBLICAÇÕES" in captured.out
        assert "8.75" in captured.out