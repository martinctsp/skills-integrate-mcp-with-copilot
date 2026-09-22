import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_valid_teacher_login_returns_success():
    response = client.post(
        "/login",
        params={"username": "admin", "password": "school123"},
    )

    assert response.status_code == 200
    assert response.json()["authenticated"] is True
    assert response.json()["username"] == "admin"


def test_invalid_teacher_login_is_rejected():
    response = client.post(
        "/login",
        params={"username": "admin", "password": "wrong-password"},
    )

    assert response.status_code == 401


def test_signup_requires_teacher_credentials():
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "student@example.com"},
    )

    assert response.status_code == 403


def test_teacher_can_signup_with_valid_credentials():
    response = client.post(
        "/activities/Chess Club/signup",
        params={
            "email": "newteacherstudent@example.com",
            "username": "admin",
            "password": "school123",
        },
    )

    assert response.status_code == 200
