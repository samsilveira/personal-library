"""
Strategy for Evaluation Report Generation
"""

from typing import List, Dict, Any
from statistics import mean, stdev
from collections import Counter
from src.models import Publication
from .report_strategy import ReportStrategy


class EvaluationReportStrategy(ReportStrategy):
    """
    Strategy for generating evaluation statistics report.
    
    Calculates:
    - Average rating
    - Standard deviation
    - Distribution by rating (0-10)
    - Most common rating
    """
    
    def generate(self, publications: List[Publication], **kwargs) -> Dict[str, Any]:
        """
        Generate evaluation statistics.
        
        Args:
            publications: List of publications
            
        Returns:
            Dictionary with evaluation statistics
        """
        # Filtrar publicações com avaliação
        evaluated = [p for p in publications if p.rating is not None]
        
        if not evaluated:
            return {
                'total_evaluated': 0,
                'average': None,
                'std_dev': None,
                'distribution': {},
                'most_common': None
            }
        
        ratings = [p.rating for p in evaluated]
        rating_counts = Counter(ratings)
        
        return {
            'total_evaluated': len(evaluated),
            'total_publications': len(publications),
            'average': round(mean(ratings), 2),
            'std_dev': round(stdev(ratings), 2) if len(ratings) > 1 else 0,
            'distribution': dict(sorted(rating_counts.items())),
            'most_common': rating_counts.most_common(1)[0],
            'min_rating': min(ratings),
            'max_rating': max(ratings)
        }
    
    def format_output(self, report_data: Dict[str, Any]) -> str:
        """Format evaluation report for display."""
        if report_data['total_evaluated'] == 0:
            return "📊 RELATÓRIO DE AVALIAÇÕES\n\nNenhuma publicação avaliada ainda."
        
        output = ["📊 RELATÓRIO DE AVALIAÇÕES\n"]
        output.append(f"Total de publicações: {report_data['total_publications']}")
        output.append(f"Publicações avaliadas: {report_data['total_evaluated']}")
        output.append(f"\n⭐ Média geral: {report_data['average']}/10")
        output.append(f"📈 Desvio padrão: {report_data['std_dev']}")
        output.append(f"🔻 Menor nota: {report_data['min_rating']}/10")
        output.append(f"🔺 Maior nota: {report_data['max_rating']}/10")
        
        most_common_rating, count = report_data['most_common']
        output.append(f"🎯 Nota mais comum: {most_common_rating}/10 ({count} publicações)")
        
        output.append("\n📊 Distribuição de notas:")
        for rating, count in report_data['distribution'].items():
            bar = '█' * count
            output.append(f"  {rating:2}/10: {bar} ({count})")
        
        return '\n'.join(output)