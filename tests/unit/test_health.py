# EN: Basic unit test for the root health endpoint.
# FR: Test unitaire basique pour l'endpoint de santé racine.

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_health() -> None:
    """
    EN: Verify that the root endpoint returns a valid health check response.
    FR: Vérifie que l'endpoint racine renvoie une réponse de santé valide.
    """
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "environment" in data
