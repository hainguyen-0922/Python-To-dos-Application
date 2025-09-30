from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.routers.auth import get_db_context

client = TestClient(app)

class DummyQuery:
    def filter(self, *args, **kwargs):
        return self

    def all(self):
        return []

class DummySession:
    def query(self, *args, **kwargs):
        return DummyQuery()

def override_get_db_context():
    return DummySession()

app.dependency_overrides[get_db_context] = override_get_db_context

@patch("services.auth.token_interceptor")
def test_get_companies(mock_auth):
    mock_auth.return_value = {"is_admin": True}
    response = client.get("/company")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
