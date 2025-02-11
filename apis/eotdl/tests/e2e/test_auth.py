import pytest
from fastapi.testclient import TestClient
from api.main import app
import os

from ...routers.auth import get_current_user
from ...src.models import User
from .setup import users, db

client = TestClient(app)

headers = {"X-API-Key": os.environ.get("ADMIN_API_KEY")}


@pytest.fixture
def url():
    yield "/auth"


def test_login(url):
    login_url = url + "/login"
    response = client.get(login_url)
    assert response.status_code == 200
    data = response.json()
    assert "login_url" in data
    assert "code" in data
    assert "message" in data


def test_logout(url):
    login_url = url + "/logout"
    response = client.get(login_url)
    assert response.status_code == 200
    logout_url = response.json()
    assert logout_url is not None


def get_current_user_mock():
    return User(**users[0])


app.dependency_overrides[get_current_user] = get_current_user_mock


def test_update_user(url, db):
    response = client.post(url, json={"name": "test3"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "test3"


def test_update_user_fails_if_user_already_exists(url, db):
    response = client.post(url, json={"name": "test"})
    assert response.status_code != 200
    data = response.json()
    assert data["detail"] == "User already exists"


def test_update_user_fails_if_invalid_data(url, db):
    response = client.post(url, json={"name": 123})
    assert response.status_code != 200
