from fastapi.testclient import TestClient
from src.endpoints.ims_api import app

client = TestClient(app)
base_url = "/ims/rest/"


def test_read_root():
    response = client.get("/")
    assert response.status_code == 404


def test_read_base_url():
    response = client.get(base_url)
    assert response.status_code == 404
