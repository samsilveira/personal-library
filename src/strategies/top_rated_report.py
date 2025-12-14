"""
Strategy for Top Rated Publications Report
"""

from typing import List, Dict, Any
from src.models import Publication, Book, Magazine
from .report_strategy import ReportStrategy


class TopRatedReportStrategy(ReportStrategy):
    """
    Strategy for generating top-rated publications report.
    
    Lists the highest-rated publications with details.
    """
    
    def generate(self, publications: List[Publication], **kwargs) -> Dict[str, Any]:
        """
        Generate top-rated publications list.
        
        Args:
            publications: List of publications
            **kwargs: Can include 'limit' (default: 5)
            
        Returns:
            Dictionary with top-rated publications
        """
        limit = kwargs.get('limit', 5)
        
        # Filtrar publicações com avaliação
        evaluated = [p for p in publications if p.rating is not None]
        
        # Ordenar por nota (decrescente) e depois por título
        top_rated = sorted(
            evaluated,
            key=lambda p: (-p.rating, p.title)
        )[:limit]
        
        return {
            'limit': limit,
            'total_evaluated': len(evaluated),
            'top_publications': [
                {
                    'id': p.id,
                    'title': p.title,
                    'author': p.author,
                    'rating': p.rating,
                    'type': 'Livro' if isinstance(p, Book) else 'Revista',
                    'year': p.year,
                    'status': p.status  # ✅ CORRIGIDO: status já é string
                }
                for p in top_rated
            ]
        }
    
    def format_output(self, report_data: Dict[str, Any]) -> str:
        """Format top-rated report for display."""
        limit = report_data['limit']
        top_pubs = report_data['top_publications']
        
        if not top_pubs:
            return f"🏆 TOP {limit} PUBLICAÇÕES\n\nNenhuma publicação avaliada ainda."
        
        output = [f"🏆 TOP {len(top_pubs)} PUBLICAÇÕES MELHOR AVALIADAS\n"]
        
        for i, pub in enumerate(top_pubs, 1):
            medal = {1: '🥇', 2: '🥈', 3: '🥉'}.get(i, f'{i}.')
            output.append(f"{medal} {pub['title']}")
            output.append(f"   Autor: {pub['author']}")
            output.append(f"   Nota: {'⭐' * int(pub['rating'])} {pub['rating']}/10")
            output.append(f"   Tipo: {pub['type']} ({pub['year']})")
            output.append(f"   Status: {pub['status']}")
            output.append("")
        
        return '\n'.join(output)