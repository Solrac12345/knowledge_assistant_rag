# EN: Unit tests for the dummy LLM dev client.
# FR: Tests unitaires pour le client LLM factice de développement.

import asyncio

import pytest

from app.llm.dummy_client import DummyLLMClient, _best_context_sentence, _parse_rag_prompt

VACATION_CONTEXT = (
    "Vacation Policy 2026\n"
    "All full-time employees are entitled to 15 working days of paid vacation per year.\n"
    "Part-time employees receive prorated vacation."
)
REMOTE_CONTEXT = "Employees may work remotely up to 3 days per week with manager approval."
GLUED_HEALTH_CONTEXT = (
    "and vision coverageEmployees can choose between PPO and HMO plans during open enrollment in November."
)
GLUED_REMOTE_CONTEXT = (
    "REMOTE WORK POLICYEmployees may work remotely up to 3 days per week with manager approval."
)
NUMBERED_SECTION_CONTEXT = (
    "2: REMOTE WORK POLICY Employees may work remotely up to 3 days per week with manager approval."
)


@pytest.mark.parametrize(
    ("context", "question", "expected"),
    [
        (
            VACATION_CONTEXT,
            "how many vacation days full-time",
            "All full-time employees are entitled to 15 working days of paid vacation per year.",
        ),
        (
            REMOTE_CONTEXT,
            "remote work days per week",
            REMOTE_CONTEXT,
        ),
    ],
)
def test_best_context_sentence(context: str, question: str, expected: str) -> None:
    assert _best_context_sentence(context, question) == expected


def test_dummy_client_returns_plain_answer() -> None:
    prompt = (
        "You are a helpful assistant. Use the following context to answer the question.\n\n"
        f"Context:\n{VACATION_CONTEXT}\n\n"
        "Question: how many vacation days full-time\n\n"
        "Answer:"
    )
    answer = asyncio.run(DummyLLMClient().generate(prompt))
    assert "\n\n" not in answer
    assert "You are a helpful assistant" not in answer
    assert "15 working days" in answer


def test_parse_rag_prompt() -> None:
    prompt = "Context:\nfoo\n\nQuestion: bar\n\nAnswer:"
    assert _parse_rag_prompt(prompt) == ("foo", "bar")


@pytest.mark.parametrize(
    ("context", "question", "expected"),
    [
        (
            GLUED_HEALTH_CONTEXT,
            "health insurance PPO HMO",
            "Employees can choose between PPO and HMO plans during open enrollment in November.",
        ),
        (
            GLUED_REMOTE_CONTEXT,
            "remote work days per week",
            "Employees may work remotely up to 3 days per week with manager approval.",
        ),
        (
            NUMBERED_SECTION_CONTEXT,
            "remote work days per week",
            "Employees may work remotely up to 3 days per week with manager approval.",
        ),
    ],
)
def test_best_context_sentence_repairs_glued_chunks(
    context: str, question: str, expected: str
) -> None:
    assert _best_context_sentence(context, question) == expected
