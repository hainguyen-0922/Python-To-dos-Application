from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.routers.auth import get_db_context

client = TestClient(app)

class DummySession:
    def __hash__(self):
        return 1

def override_get_db_context():
    return DummySession()

app.dependency_overrides[get_db_context] = override_get_db_context

class DummyUser:
    def __init__(self, username="testuser"):
        self.username = username
        self.id = 1
        self.is_active = True

@patch("services.auth.create_access_token")
@patch("services.auth.authenticate")
def test_login_success(mock_authenticate, mock_create_token):
    mock_user = DummyUser()
    mock_authenticate.return_value = mock_user
    mock_create_token.return_value = "fake_token"

    response = client.post(
        "/auth/token",
        data={"username": "testuser", "password": "testpass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    assert response.status_code == 200
    assert response.json()["access_token"] == "fake_token"
