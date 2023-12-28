import pytest
from fastapi.testclient import TestClient

from src.app import app


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as test_client:
        yield test_client
