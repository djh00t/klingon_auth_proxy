import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Redirecting / request to /login"}

def test_login_get():
    response = client.get("/login")
    assert response.status_code == 200

def test_login_post():
    response = client.post("/login", data={"username": "test", "password": "test"})
    assert response.status_code == 200
    assert response.json() == {"message": "Credentials are valid"}
