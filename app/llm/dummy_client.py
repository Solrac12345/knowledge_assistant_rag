# EN: Concrete LLM client implementations.
# FR: Implémentations concrètes des clients LLM.

import re

from app.llm.base import LLMClient

_CONTEXT_MARKER = "Context:\n"
_QUESTION_MARKER = "\n\nQuestion:"
_ANSWER_MARKER = "\n\nAnswer:"


def _parse_rag_prompt(prompt: str) -> tuple[str, str]:
    """EN: Extract context and question from the RAG pipeline prompt."""
    if _CONTEXT_MARKER not in prompt or _QUESTION_MARKER not in prompt:
        return "", ""
    rest = prompt.split(_CONTEXT_MARKER, 1)[1]
    context, rest = rest.split(_QUESTION_MARKER, 1)
    question = rest.split(_ANSWER_MARKER, 1)[0].strip()
    return context.strip(), question


def _normalize_context(text: str) -> str:
    """EN: Repair common chunk-boundary glues before sentence extraction."""
    text = re.sub(r"\.([A-Z])", r". \1", text)
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
    text = re.sub(r"([A-Z]{2,})([A-Z][a-z])", r"\1 \2", text)
    return text


_SECTION_HEADER_PREFIX = re.compile(
    r"^(?:SECTION\s+\d+:\s*)?(?:\d+:\s*)?(?:[A-Z][A-Z0-9\s:\-]*?)(?=\s*[A-Z][a-z])"
)


def _clean_answer_sentence(sentence: str) -> str:
    """EN: Drop section titles glued to the start of a policy sentence."""
    cleaned = re.sub(
        r"^(?:(?:SECTION\s+)?\d+\s*:\s*)+",
        "",
        sentence,
        flags=re.IGNORECASE,
    ).strip()
    cleaned = _SECTION_HEADER_PREFIX.sub("", cleaned, count=1).strip()
    cleaned = re.sub(r"^:\s*", "", cleaned).strip()
    return cleaned or sentence


def _is_valid_answer_sentence(sentence: str) -> bool:
    sentence = _clean_answer_sentence(sentence)
    if len(sentence) < 25:
        return False
    if re.match(r"^SECTION\s+\d+:", sentence, re.IGNORECASE):
        return False
    if re.fullmatch(r"[A-Z0-9\s:\-]+", sentence):
        return False
    if (
        re.search(r"\b(?:policy|section)\s+\d{4}\b", sentence, re.IGNORECASE)
        and "." not in sentence
    ):
        return False
    if sentence[0].islower():
        return False
    return True


def _extract_sentences(context: str) -> list[str]:
    """EN: Extract complete sentences from retrieved context blocks."""
    normalized = _normalize_context(context)
    sentences: list[str] = []
    seen: set[str] = set()

    for match in re.finditer(r"[A-Z][^\n.!?]{24,}[.!?]", normalized):
        sentence = _clean_answer_sentence(match.group(0).strip())
        if _is_valid_answer_sentence(sentence) and sentence not in seen:
            seen.add(sentence)
            sentences.append(sentence)

    return sentences


def _best_context_sentence(context: str, question: str) -> str:
    """EN: Pick the retrieved sentence that best matches the user question."""
    candidates = _extract_sentences(context)
    if not candidates:
        return "No relevant information found in the indexed documents."

    question_words = {w.lower() for w in re.findall(r"\w+", question) if len(w) > 2}

    def score(sentence: str) -> int:
        sentence_words = {w.lower() for w in re.findall(r"\w+", sentence)}
        overlap = len(question_words & sentence_words)
        sentence_upper = sentence.upper()
        for token in re.findall(r"\w+", question):
            if len(token) <= 4 and token.upper() in sentence_upper:
                overlap += 2
        return overlap

    return max(candidates, key=score)


class DummyLLMClient(LLMClient):
    """
    EN: Simple placeholder LLM client used during early development.
    FR: Client LLM factice utilisé pendant le développement initial.
    """

    async def generate(self, prompt: str) -> str:
        """
        EN: Return a short answer derived from retrieved context (dev mode).
        FR: Retourner une courte réponse dérivée du contexte récupéré (mode dev).
        """
        context, question = _parse_rag_prompt(prompt)
        if not context:
            return "[dev mode] Dummy LLM received a non-RAG prompt; configure a real provider for production."
        return _best_context_sentence(context, question)
