import pytest

from src.test.end_to_end.helper import Helper
from src.test.end_to_end.test_main import client


@pytest.fixture()
def get_user_dict():
    user = Helper.get_secret_regular()
    user_dict = {
        "username": user["email"],
        "password": user["password"]
    }
    return user_dict


def test_token(get_user_dict):
    _ = Helper.get_user_id()  # To create a user
    response = client.post("/token", data=get_user_dict)
    if response.status_code == 401:
        Helper.create_user(get_user_dict["username"], "NetOps", Helper.get_secret_regular()["hash"])
        response = client.post("/token", data=get_user_dict)
    assert response.status_code == 200, response.text


@pytest.mark.order(after="test_token")
def test_user_login(get_user_dict):
    _ = Helper.get_user_id()  # To create a user
    response = client.post("/login", json=get_user_dict)
    assert response.status_code == 200, response.text


@pytest.mark.order(after="test_user_login")
def test_bad_user_login():
    user_dict = {
        "username": "test@exa.com",
        "password": Helper.get_secret_regular()["password"]
    }
    _ = Helper.get_user_id()  # To create a user
    response = client.post("/login", json=user_dict)
    assert response.status_code == 401, response.text
