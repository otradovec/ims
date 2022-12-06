import pytest, json
from src.test.end_to_end.test_main import client, base_url
from src.test.end_to_end.helper import Helper


@pytest.mark.order("first")
def test_read_users_empty():
    response = client.get(base_url + "users?skip=0&limit=100")
    assert response.status_code == 200, "Empty user list"


@pytest.mark.order("first")
def test_read_users_empty_with_search():
    response = client.get(base_url + "users?skip=0&limit=100&user_search=mining")
    assert response.status_code == 200, "Empty user list"


@pytest.mark.order("second")
def test_crud_user():
    json_create = {
        "email": "klement@hofbauer.com",
        "user_role": "NetOps",
        "hashed_password": "string"
    }
    response = client.post(url=base_url + "users", json=json_create)
    assert response.status_code == 200, "User created" + response.text
    user_id = json.loads(response.text)["user_id"]

    response = client.get(base_url + f"users/{user_id}")
    assert response.status_code == 200, "User detail" + response.text
    assert "klement" in response.text

    updated_json = {
        "user_id": user_id,
        "email": "klement@hofbauer.com",
        "user_role": "Manager",
        "is_active": True
    }
    response = client.put(url=base_url + "users", json=updated_json)
    assert response.status_code == 200, "User updated " + response.text

    response = client.put(url=base_url + f"users/{user_id}/passwd?hashed_password=anotherpass")
    assert response.status_code == 200, "User pass updated " + response.text

    response = client.delete(url=base_url + f"users/{user_id}")
    assert response.status_code == 200, "User deleted " + response.text


@pytest.mark.order("third")
def test_user_list():
    user_id = Helper.get_user_id()
    response = client.get(base_url+f"users/{user_id}")
    email: str = json.loads(response.text)["email"]

    response = client.get(url=base_url + f"users?skip=0&limit=100&user_search={email}")
    assert response.status_code == 200  # User list with search
    assert email in response.text
    assert str(user_id) in response.text

    email_part = email[0:3]
    response = client.get(url=base_url + f"users?skip=0&limit=100&user_search={email_part}")
    assert response.status_code == 200  # User list with partial search
    assert email_part in response.text

    response = client.get(url=base_url + f"users?skip=-5&limit=100&user_search={email_part}")
    assert response.status_code == 422


def test_user_roles():
    response = client.get(url=base_url + f"user-roles")
    assert response.status_code == 200
    assert '"Support":1,' in response.text
