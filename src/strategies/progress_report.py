"""
Strategy for Annual Progress Report
"""

from typing import List, Dict, Any
from datetime import datetime
from src.models import Publication, Configuration
from .report_strategy import ReportStrategy


class ProgressReportStrategy(ReportStrategy):
    """
    Strategy for generating annual reading progress report.
    
    Tracks progress towards annual reading goal.
    """
    
    def generate(self, publications: List[Publication], **kwargs) -> Dict[str, Any]:
        """
        Generate annual progress report.
        
        Args:
            publications: List of publications
            **kwargs: Must include 'config' (Configuration object)
            
        Returns:
            Dictionary with progress data
        """
        config: Configuration = kwargs.get('config')
        if not config:
            raise ValueError("Configuration required for progress report")
        
        current_year = datetime.now().year
        
        # Publicações finalizadas no ano atual
        finished_this_year = [
            p for p in publications
            if p.end_read_date and p.end_read_date.year == current_year
        ]
        
        # Publicações em leitura
        currently_reading = [
            p for p in publications
            if p.start_read_date and not p.end_read_date
        ]
        
        # Calcular progresso
        total_finished = len(finished_this_year)
        goal = config.annual_goal
        percentage = (total_finished / goal * 100) if goal > 0 else 0
        remaining = max(0, goal - total_finished)
        
        # Calcular média de páginas
        pages_read = sum(
            p.number_of_pages for p in finished_this_year
            if hasattr(p, 'number_of_pages') and p.number_of_pages
        )
        avg_pages = pages_read / total_finished if total_finished > 0 else 0
        
        return {
            'year': current_year,
            'goal': goal,
            'completed': total_finished,
            'percentage': round(percentage, 1),
            'remaining': remaining,
            'currently_reading': len(currently_reading),
            'limit': config.simultaneous_reading_limit,
            'pages_read': pages_read,
            'avg_pages': round(avg_pages, 0),
            'finished_publications': [
                {
                    'title': p.title,
                    'author': p.author,
                    'finish_date': p.end_read_date.strftime('%d/%m/%Y')
                }
                for p in sorted(finished_this_year, key=lambda x: x.end_read_date)
            ],
            'reading_publications': [
                {
                    'title': p.title,
                    'author': p.author,
                    'start_date': p.start_read_date.strftime('%d/%m/%Y')
                }
                for p in currently_reading
            ]
        }
    
    def format_output(self, report_data: Dict[str, Any]) -> str:
        """Format progress report for display."""
        output = [f"📈 PROGRESSO ANUAL DE LEITURA - {report_data['year']}\n"]
        
        # Meta
        output.append(f"🎯 Meta: {report_data['goal']} publicações/ano")
        output.append(f"✅ Concluídas: {report_data['completed']}")
        output.append(f"📊 Progresso: {report_data['percentage']}%")
        
        # Barra de progresso
        total_bars = 20
        filled_bars = int(report_data['percentage'] / 100 * total_bars)
        bar = '█' * filled_bars + '░' * (total_bars - filled_bars)
        output.append(f"   [{bar}]")
        
        output.append(f"⏳ Faltam: {report_data['remaining']} publicações")
        
        # Leituras simultâneas
        output.append(f"\n📚 Leituras atuais: {report_data['currently_reading']}/{report_data['limit']}")
        
        # Estatísticas
        output.append(f"\n📖 Páginas lidas: {report_data['pages_read']:,}")
        if report_data['completed'] > 0:
            output.append(f"📄 Média de páginas: {report_data['avg_pages']:.0f} páginas/publicação")
        
        # Publicações finalizadas
        if report_data['finished_publications']:
            output.append("\n✅ Publicações finalizadas este ano:")
            for pub in report_data['finished_publications'][-5:]:  # Últimas 5
                output.append(f"   • {pub['title']} - {pub['author']} ({pub['finish_date']})")
        
        # Publicações em andamento
        if report_data['reading_publications']:
            output.append("\n📖 Lendo atualmente:")
            for pub in report_data['reading_publications']:
                output.append(f"   • {pub['title']} - {pub['author']} (desde {pub['start_date']})")
        
        return '\n'.join(output)