"""
Module containing data persistinf functions.
"""
import sys
import json
import sqlite3
from typing import List
from datetime import date
from pathlib import Path
from src.models import Collection, Publication, Annotation

def _get_data_filepath(filename: str = "library.json") -> Path:
    """
    Get absolute path to data file in project root.

    Args:
        filename: Name of the data file

    Returns:
        Resolved Path object to the file
    """
    return (Path(__file__).parent.parent.parent / filename).resolve()

def save_publication(publications: List[Publication], filepath: str = "library.json") -> None:
    """
    Save a publication to JSON file.

    Args:
        publications: List of Publication objects to save
        filepath: Filename (will be saved in project root)
    """
    full_path = _get_data_filepath(filepath)

    data = [pub.to_dict() for pub in publications]

    full_path.parent.mkdir(parents=True, exist_ok=True)

    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"✅ {len(publications)} publicações salvas em: {full_path}")

def load_publications(filepath: str = "library.json") -> List[Publication]:
    """
    Load all publications from JSON file.

    Args:
        filepath: Filename (will be loaded from project root)

    Returns:
        List of Publication objects (Book or Magazine instances)

    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If file is not valid JSON
    """
    full_path = _get_data_filepath(filepath)

    try:
        with open(full_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        publications = [Publication.from_dict(pub_dict) for pub_dict in data]

        print(f"✅ {len(publications)} publicações carregadas de: {full_path}")
        return publications
    
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {full_path}")
        print("Retornando lista vazia (primeira execução?)")
        return []
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        print(f"Arquivo corrompido: {full_path}")
        raise
    
    except Exception as e:
        print(f"Erro inesperado ao carregar publicações: {e}")
        raise

def save_collection(collection: Collection, filepath: str = "library.json") -> None:
    """
    Save all publications in a JSON file.
    """
    full_path = _get_data_filepath(filepath)
    publications = collection.list_publications()
    data = [pub.to_dict() for pub in publications]

    full_path.parent.mkdir(parents=True, exist_ok=True)

    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"{len(publications)} salvas em {full_path}")

def load_collection(filepath: str = "library.json") -> Collection:
    """
    Load collection from a JSON file.
    """
    full_path = _get_data_filepath(filepath)
    collection = Collection()

    try:
        with open(full_path, "r", encoding="utf-8") as f:
            data = json.load(f)

            for pub_data in data:
                pub = Publication.from_dict(pub_data)
                collection.register_publication(pub)

        print(f"{len(data)} publicações carregadas de {full_path}")

    except FileNotFoundError:
        print(f"Arquivo não encontrado: {full_path}")
        print("Retornando collection vazia (primeira execução)")

    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        raise

    return collection

'''

Para implementação posterior com SQLite
def save_publication(conn: sqlite3.Connection, publication: Publication) -> bool:
    """
    Save a publication to the database.

    Args:
        conn: Datavase connection
        publication: Publication object to save

    Returns:
        True if saved sucessfully, False otherwise
    """
    pass

def load_publications(conn: sqlite3.Connection) -> List[Publication]:
    """
    Load all publications from the database.

    Args:
        conn: Database connection

    Returns:
        List of Publication object
    """
    pass

def update_publication(conn: sqlite3.Connection, publication: Publication) -> bool:
    """
    Update an existing publication in the database.

    Args:
        conn: Database connection
        publication: Publication object with updated data

    Returns:
        True if updated sucessfully, False otherwise
    """
    pass

def delete_publication(conn: sqlite3.Connection, publication_id: str) -> bool:
    """
    Delete a publication from the database.

    Args:
        conn: Database connection
        publication_id: ID of publication to delete

    Returns:
        True if deleted sucessfully, False otherwise
    """
    pass

def save_anntotation(conn: sqlite3.Connection, publication_id: str, annotation: Annotation) -> bool:
    """
    Save an annotation to the database.

    Args:
        conn: Database connection
        publication_id: ID of the associated publication
        annotation: Annotation object to save

    Returns:
        True if saved sucessfully, False otherwise
    """
    pass

def load_annotatios(conn: sqlite3.Connection, publication_id: str) -> List[Annotation]:
    """
    Load all annotations for a specific publication.

    Args:
        conn: Database connection
        publication_id: ID of the publication
    
    Returns:
        List of Annotation objects
    """
    pass
'''