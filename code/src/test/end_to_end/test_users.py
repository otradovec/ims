import pytest
from src.test.end_to_end.test_main import client, base_url


@pytest.mark.order("first")
def test_read_users_empty():
    response = client.get(base_url + "users?skip=0&limit=100")
    assert response.status_code == 200, "Empty user list"


@pytest.mark.order("second")
def test_crud_user():
    response = client.get(base_url+"users/1")
    assert response.status_code == 404  # User not yet created
    json_create = {
        "email": "klement@hofbauer.com",
        "user_role": 2,
        "hashed_password": "string"
    }
    response = client.post(url=base_url + "users", json=json_create)
    assert response.status_code == 200  # User created

    response = client.get(base_url + "users/1")
    assert response.status_code == 200  # User detail
    assert "klement" in response.text

    updated_json = {
        "user_id": 1,
        "email": "klement@hofbauer.com",
        "user_role": 3,
        "is_active": True
    }
    response = client.put(url=base_url + "users", json=updated_json)
    assert response.status_code == 200, "User updated " + response.text

    response = client.put(url=base_url + "users/1/passwd?hashed_password=anotherpass")
    assert response.status_code == 200, "User pass updated " + response.text

    response = client.delete(url=base_url + "users/1")
    assert response.status_code == 200, "User deleted " + response.text
