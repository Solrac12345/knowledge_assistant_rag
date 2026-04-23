# EN: Basic unit test for the RAG placeholder endpoint.
# FR: Test unitaire basique pour l'endpoint placeholder du RAG.

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_rag_placeholder() -> None:
    """
    EN: Verify that the RAG placeholder endpoint returns the expected message.
    FR: Vérifie que l'endpoint placeholder RAG renvoie le message attendu.
    """
    response = client.get("/api/v1/rag/placeholder")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "RAG API placeholder"
