# EN: Integration tests for the RAG API endpoints.
# FR: Tests d'intégration pour les endpoints de l'API RAG.

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def client() -> TestClient:
    """
    EN: Fixture that manages TestClient lifecycle with lifespan support.
    FR: Fixture qui gère le cycle de vie de TestClient avec support du lifespan.
    """
    with TestClient(app) as test_client:
        yield test_client


def test_health_check(client: TestClient) -> None:
    """
    EN: Verify the root health endpoint returns 200 OK.
    FR: Vérifier que l'endpoint racine renvoie 200 OK.
    """
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_index_document(client: TestClient) -> None:
    """
    EN: Test uploading a document and verifying the indexing response.
    FR: Tester l'upload d'un document et vérifier la réponse d'indexation.
    """
    # Create a dummy file in memory
    file_content = b"This is a test document for the RAG system. It contains AI context."
    file_data = {"file": ("test_sol.txt", file_content, "text/plain")}

    # Send POST request to the index endpoint
    response = client.post("/api/v1/rag/index", files=file_data)

    # Assert response
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "indexed"
    assert data["filename"] == "test_sol.txt"


def test_ask_question_structure(client: TestClient) -> None:
    """
    EN: Test the query endpoint structure (returns valid JSON with answer).
    FR: Tester la structure de l'endpoint de requête (renvoie un JSON valide avec réponse).
    """
    # Note: This test checks the structure. If LLM_PROVIDER=dummy,
    # the answer will be the dummy response.
    response = client.get("/api/v1/rag/ask", params={"query": "What is this document?"})

    assert response.status_code == 200
    data = response.json()

    # Validate Pydantic Model structure
    assert "query" in data
    assert "answer" in data
    assert data["query"] == "What is this document?"
    assert isinstance(data["answer"], str)


def test_ask_question_empty_query(client: TestClient) -> None:
    """
    EN: Test that an empty query returns a 400 Bad Request error.
    FR: Vérifier qu'une requête vide renvoie une erreur 400 Bad Request.
    """
    response = client.get("/api/v1/rag/ask", params={"query": "   "})

    assert response.status_code == 400
    assert "Query cannot be empty" in response.json()["detail"]
