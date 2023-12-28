from fastapi.testclient import TestClient


def test_ping(client: TestClient) -> None:
    """
    test ping endpoint
    """

    response = client.get("/api/ping")
    assert response.status_code == 200
    assert response.text == '"ok"'
