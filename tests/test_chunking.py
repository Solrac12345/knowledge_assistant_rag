# EN: Unit tests for text chunking overlap behavior.
# FR: Tests unitaires pour le comportement de chevauchement du découpage.

from app.rag.chunking import _apply_overlap, _merge_with_overlap, recursive_chunk


def test_merge_with_overlap_inserts_space() -> None:
    merged = _merge_with_overlap("and vision coverage", "Employees can choose")
    assert merged == "and vision coverage Employees can choose"


def test_apply_overlap_does_not_glue_words() -> None:
    chunks = [
        "medical, dental, and vision coverage.",
        "Employees can choose between PPO and HMO plans.",
    ]
    result = _apply_overlap(chunks, overlap=20)
    assert "coverageEmployees" not in result[1]
    assert " " in result[1]


def test_recursive_chunk_keeps_policy_sentence_intact() -> None:
    text = (
        "SECTION 3: HEALTH BENEFITS\n"
        "The company provides comprehensive health insurance including medical, dental, and vision coverage. "
        "Employees can choose between PPO and HMO plans during open enrollment in November."
    )
    chunks = recursive_chunk(text, chunk_size=256, chunk_overlap=40)
    joined = " ".join(chunks)
    assert "coverageEmployees" not in joined
    assert "PPO and HMO" in joined
