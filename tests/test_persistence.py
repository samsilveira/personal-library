"""Publication persistence test."""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from models import Book, Magazine, Annotation
from data import save_publication, load_publications

def test_save_and_load():
    """Test complete save/load cycle."""
    print("=" * 50)
    print("TESTE DE PERSISTÊNCIA")
    print("=" * 50)

    print("\nCriando publicações de teste...")

    book1 = Book(
        pub_id=1, 
        title="1984", 
        author="George Orwell", 
        publisher="Secker & Warburg", 
        year=1949, 
        genre="Dystopian Fiction", 
        number_of_pages=328, 
        isbn="978-0451524935",
        edition=1,
        file_path="/books/1984.pdf"
    )
        
    book1.start_reading()

    annotation = Annotation(
        annotation_id=1,
        text="Powerful opening", 
        reference_excerpt="It was a bright cold day in April..."
    )
    book1.add_annotation(annotation)
    book1.finish_reading()
    book1.rate_publication(5)

    mag1 = Magazine(
        pub_id=2,
        title="National Geographic",
        author="Various",
        publisher="National Geographic Society",
        year=2024,
        genre="Science",
        number_of_pages=100,
        issn="0027-9358",
        issue_number=12,
        file_path="/magazines/natgeo_dec2024.pdf"
    )

    publications = [book1, mag1]

    print("\nSalvando publicações...")
    save_publication(publications)

    print("\nCarregando publicações")
    loaded_pubs = load_publications()

    print("\nVALIDAÇÃO:")
    print(f"    Publicações salvas: {len(publications)}")
    print(f"    Publicações carregadas: {len(loaded_pubs)}")

    loaded_book = loaded_pubs[0]
    print("\nLivro carregado:")
    print(f"    Título: {loaded_book.title}") 
    print(f"    Status: {loaded_book.status}") 
    print(f"    Rating: {loaded_book.rating}") 
    print(f"    Anotações: {len(loaded_book.list_annotations())}") 

    if loaded_book.list_annotations():
        ann = loaded_book.list_annotations()[0]
        print(f"    Primeira anotação: {ann.text}")

    print("=" * 50)
    print("TESTE CONCLUIDO")
    print("=" * 50)

if __name__ == "__main__":
    test_save_and_load()