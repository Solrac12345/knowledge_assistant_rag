# EN: Text chunking utilities for the RAG pipeline.
# FR: Utilitaires de découpage de texte pour le pipeline RAG.

import re


def recursive_chunk(
    text: str,
    chunk_size: int = 256,
    chunk_overlap: int = 40,
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
    text = re.sub(r"\.([A-Z])", r". \1", text)

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


def _overlap_prefix(previous: str, overlap: int) -> str:
    """
    EN: Take a suffix for overlap, aligned to a word boundary.
    FR: Prendre un suffixe pour le chevauchement, aligné sur une limite de mot.
    """
    if overlap <= 0:
        return ""
    prefix = previous[-overlap:]
    word_start = prefix.find(" ")
    if word_start != -1:
        prefix = prefix[word_start + 1 :]
    return prefix


def _merge_with_overlap(prefix: str, chunk: str) -> str:
    """
    EN: Join overlap prefix and chunk without gluing words together.
    FR: Joindre le préfixe de chevauchement et le bloc sans coller les mots.
    """
    if not prefix:
        return chunk
    if chunk.startswith(prefix):
        return chunk
    needs_space = (
        prefix[-1].isalnum()
        and chunk[0].isalnum()
        and not prefix.endswith(" ")
        and not chunk.startswith(" ")
    )
    return f"{prefix} {chunk}" if needs_space else prefix + chunk


def _apply_overlap(chunks: list[str], overlap: int) -> list[str]:
    """
    EN: Add word-aware overlap between consecutive chunks.
    FR: Ajouter un chevauchement conscient des mots entre les blocs consécutifs.
    """
    if overlap <= 0 or len(chunks) <= 1:
        return chunks

    result: list[str] = [chunks[0]]

    for i in range(1, len(chunks)):
        prefix = _overlap_prefix(chunks[i - 1], overlap)
        result.append(_merge_with_overlap(prefix, chunks[i]))

    return result
