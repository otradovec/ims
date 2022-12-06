import pytest

from src.test.end_to_end.helper import Helper
from src.test.end_to_end.test_main import client


@pytest.mark.order("first")
def test_token():
    user_dict = {
        "username": "test@example.com",
        "password": Helper.get_secret()["password"]
    }
    Helper.get_user_id()  # To create a user
    response = client.post("/token", data=user_dict)
    assert response.status_code == 200, response.text
