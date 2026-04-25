# EN: Text chunking utilities for the RAG pipeline.
# FR: Utilitaires de découpage de texte pour le pipeline RAG.



def recursive_chunk(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
    separators: list[str] | None = None,
) -> list[str]:
    """
    EN: Split text into overlapping chunks using recursive semantic separators.
    FR: Découper le texte en blocs chevauchants en utilisant des séparateurs sémantiques récursifs.

    Args:
        text: The input text to chunk.
        chunk_size: Maximum characters per chunk.
        chunk_overlap: Characters to overlap between chunks (preserves context).
        separators: Priority order of separators to split on.

    Returns:
        List of text chunks ready for embedding.
    """
    if separators is None:
        # EN: Split by semantic boundaries, from most to least preferred.
        # FR: Découper par frontières sémantiques, du plus au moins prioritaire.
        separators = ["\n\n", "\n", ". ", "! ", "? ", " ", ""]

    # Base case: text fits in one chunk
    if len(text) <= chunk_size:
        return [text.strip()] if text.strip() else []

    # Try splitting by each separator in priority order
    for sep in separators:
        if sep:
            parts = text.split(sep)
        else:
            # Fallback: split by character if all else fails
            parts = list(text)

        # If splitting actually created smaller parts, recurse
        if len(parts) > 1 and any(len(p) < len(text) for p in parts):
            chunks: list[str] = []
            current = ""

            for part in parts:
                part = part.strip()
                if not part:
                    continue

                # If adding this part exceeds chunk_size, save current and start new
                if len(current) + len(part) + len(sep) > chunk_size:
                    if current:
                        chunks.append(current)
                    # Handle oversized single parts by recursing deeper
                    if len(part) > chunk_size:
                        chunks.extend(
                            recursive_chunk(part, chunk_size, chunk_overlap, separators[1:])
                        )
                    else:
                        current = part
                else:
                    current = current + sep + part if current else part

            if current:
                chunks.append(current)

            # Apply overlap for context preservation
            if chunk_overlap > 0 and len(chunks) > 1:
                return _apply_overlap(chunks, chunk_overlap)

            return chunks

    # Fallback: return as single chunk if nothing worked
    return [text.strip()] if text.strip() else []


def _apply_overlap(chunks: list[str], overlap: int) -> list[str]:
    """
    EN: Add character-level overlap between consecutive chunks.
    FR: Ajouter un chevauchement au niveau des caractères entre les blocs consécutifs.
    """
    if overlap <= 0:
        return chunks

    result: list[str] = []
    for i, chunk in enumerate(chunks):
        if i == 0:
            result.append(chunk)
        else:
            # Take the last `overlap` chars from previous chunk as prefix
            prefix = chunks[i - 1][-overlap:]
            result.append(prefix + chunk)
    return result
