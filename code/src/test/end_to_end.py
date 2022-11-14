from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)
base_url = "/ims/rest/"


def test_read_root():
    response = client.get("/")
    assert response.status_code == 404


def test_read_base_url():
    response = client.get(base_url)
    assert response.status_code == 404


def test_crud_user():
    response = client.get(base_url+"users?skip=0&limit=100")
    print(response.url)
    assert response.status_code == 200  # Empty user list
    response = client.get(base_url+"users/1")
    assert response.status_code == 404  # User not yet created
    json = {
        "email": "klement@hofbauer.com",
        "user_role": 2,
        "hashed_password": "string"
    }

    response = client.post(url=base_url + "users", json=json)
    print(response.text)

    assert response.status_code == 200  # User created
    response = client.get(base_url + "users/1")
    assert response.status_code == 200  # User detail


