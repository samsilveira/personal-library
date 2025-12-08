"""
Module containing the Report class.
"""

from typing import Dict, List, Tuple
from datetime import date
from .collection import Collection
from .publication import Publication
from .configuration import Configuration

class Report:
    """
    Stateless service class responsible for generating metrics and reports.

    Process data from a Collection to produce various statics about the user's reading habits and library composition.
    """

    @staticmethod
    def check_total_publications(collection: Collection) -> int:
        """
        Count total number of publications in the collection.

        Args:
            collection: Collection to analyze
        
        Returns:
            Total number of publications
        """
        return len(collection.list_publications())

    @staticmethod
    def check_publications_by_status(collection: Collection) -> Dict[str, Tuple[int, float]]:
        """
        Calculate quantity and percentage of publicatons by status.

        Args:
            collections: Collections to analyze

        Returns:
            Dictionary with status as key and tuple (count, percentage) as value
            Example: {"UNREAD": (7, 35.0), "READING": (3, 15.0), "READ": (10, 50.0)}
        """
        total = Report.check_total_publications(collection)
        statuses = ["UNREAD", "READING", "READ"]
        if total == 0:
            return {"UNREAD": (0, 0.0), "READING": (0, 0.0), "READ": (0, 0.0)}
        return {
            status: (
                count := len(collection.search_by_status(status)),
                (count / total * 100) if total > 0 else 0.0
            )
            for status in statuses
        }

    @staticmethod
    def calculate_average_rating(collection: Collection) -> float:
        """
        Calculate average rating of all read publications.

        Args:
            collection: Collection to analyze
        
        Returns:
            Average rating (0-10), or 0 if no rated publications exist
        """
        ratings = [pub.rating for pub in collection.search_by_status("READ") if pub.rating is not None]

        return sum(ratings) / len(ratings) if ratings else 0.0

    @staticmethod
    def check_top_5_publications(collection: Collection) -> List[Publication]:
        """
        Get the top 5 highest-rated publications.

        Args:
            collection: Collection to analyze

        Returns:
            List of up to 5 publications sorted by rating (highest first)
        """
        return sorted([pub for pub in collection.search_by_status("READ") if pub.rating is not None],
                         key=lambda pub : pub.rating,
                         reverse=True)[:5]

    @staticmethod
    def check_annual_goal_progress(collection: Collection, configuration: Configuration) -> Dict[str, any]:
        """
        Check progress towards annual reading goal.

        Args:
            collection: Collection to analyze
            configuration: Configuration with annual goal

        Returns:
            Dictionary with keys:
            - 'goal': targer number
            - 'completed': books read this year
            - 'remaining': books still needed
            - 'percentage': progress percentage
            - 'on_track': boolena indicating if on pace
        """
        pass

    @staticmethod
    def print_status_report(collection: Collection) -> None:
        """
        Print formatted status report to console.

        Args:
            collection: Collection to analyze
        """
        total = Report.check_total_publications(collection)
        by_status = Report.check_publications_by_status(collection)

        print("\n" + "=" * 60)
        print("RELATÓRIO DE PUBLICAÇÕES POR STATUS")
        print("=" * 60)
        print(f"\nTotal de Publicações: {total} ")

        if total == 0:
            print("\nNenhuma publicação cadastrada.")
            print("=" * 60 + "\n")
            return
        
        print("\n" + "-" * 60)

        status_info = {
            "UNREAD": "Não Lidos",
            "READING": "Lendo",
            "READ": "Lidos"
        }
        for status in ["UNREAD", "READING", "READ"]:
            count, percentage = by_status[status]
            label = status_info[status]
            
            bar_length = int(percentage / 2.5) if percentage > 0 else 0
            bar = "█" * bar_length
            empty_bar = "░" * (40 - bar_length)
            
            print(f"\n{label:12} │ {count:3} pub. │ {percentage:5.1f}% │ {bar}{empty_bar}")
        
        print("\n" + "="*60 + "\n")

    @staticmethod
    def print_full_report(collection: Collection) -> None:
        """
        Print comprehensive report with multiple metrics.

        Args:
            collection: Collection to analyze
        """
        total = Report.check_total_publications(collection)
        by_status = Report.check_publications_by_status(collection)
        avg_rating = Report.calculate_average_rating(collection)
        top_5 = Report.check_top_5_publications(collection)
        
        print("\n" + "="*70)
        print("📊 RELATÓRIO COMPLETO DA BIBLIOTECA")
        print("="*70)
        
        print("\n📈 ESTATÍSTICAS GERAIS")
        print("-"*70)
        print(f"  📚 Total de Publicações: {total}")
        
        if total > 0:
            read_count = by_status["READ"][0]
            read_percentage = by_status["READ"][1]
            print(f"  ✅ Publicações Lidas: {read_count} ({read_percentage:.1f}%)")
            
            if avg_rating > 0:
                print(f"  ⭐ Avaliação Média: {avg_rating:.2f}/10")
        
        print("\n📊 DISTRIBUIÇÃO POR STATUS")
        print("-"*70)
        
        status_info = {
            "UNREAD": ("📖", "Não Lidos"),
            "READING": ("📗", "Lendo"),
            "READ": ("✅", "Lidos")
        }
        
        for status in ["UNREAD", "READING", "READ"]:
            count, percentage = by_status[status]
            emoji, label = status_info[status]
            
            bar_length = int(percentage / 2) if percentage > 0 else 0
            bar = "█" * bar_length
            
            print(f"  {emoji} {label:12} │ {count:3} │ {percentage:5.1f}% │ {bar}")
        
        if top_5:
            print("\n⭐ TOP 5 PUBLICAÇÕES MAIS BEM AVALIADAS")
            print("-"*70)
            
            for i, pub in enumerate(top_5, 1):
                stars = "⭐" * int(pub.rating / 2)
                print(f"  {i}. {pub.title[:45]:45} │ {pub.rating:.1f}/10 {stars}")
        
        print("\n" + "="*70 + "\n")

    @staticmethod
    def generate_status_report_dict(collection: Collection) -> Dict:
        """
        Generate status report as a dictionary (useful for JSON export or APIs).

        Args:
            collection: Collection to analyze

        Returns:
            Dictionary with report data
        """
        total = Report.check_total_publications(collection)
        by_status = Report.check_publications_by_status(collection)
        
        return {
            "total_publications": total,
            "by_status": {
                "unread": {
                    "count": by_status["UNREAD"][0],
                    "percentage": round(by_status["UNREAD"][1], 2)
                },
                "reading": {
                    "count": by_status["READING"][0],
                    "percentage": round(by_status["READING"][1], 2)
                },
                "read": {
                    "count": by_status["READ"][0],
                    "percentage": round(by_status["READ"][1], 2)
                }
            },
            "generated_at": date.today().isoformat()
        }