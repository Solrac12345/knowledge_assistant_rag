# EN: Document ingestion utilities for the RAG pipeline.
# FR: Utilitaires d'ingestion de documents pour le pipeline RAG.

from pathlib import Path


def load_text_file(path: str | Path) -> str:
    """
    EN: Load a plain text file and return its content.
    FR: Charger un fichier texte et retourner son contenu.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return path.read_text(encoding="utf-8")


def load_pdf_file(path: str | Path) -> str:
    """
    EN: Placeholder for PDF ingestion.
    FR: Espace réservé pour l'ingestion de PDF.
    """
    # EN: In Phase 3, we will integrate pypdf or pdfminer.
    # FR: En Phase 3, nous intégrerons pypdf ou pdfminer.
    raise NotImplementedError("PDF ingestion not implemented yet.")


def ingest_document(path: str | Path) -> str:
    """
    EN: Generic ingestion function that detects file type.
    FR: Fonction d'ingestion générique qui détecte le type de fichier.
    """
    path = Path(path)
    suffix = path.suffix.lower()

    match suffix:
        case ".txt" | ".md":
            return load_text_file(path)
        case ".pdf":
            return load_pdf_file(path)
        case _:
            raise ValueError(f"Unsupported file type: {suffix}")
