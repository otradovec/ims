import json
import pytest

from src.test.end_to_end.helper import Helper
from src.test.end_to_end.test_main import client, base_url

good_header = Helper.get_header_with_token()
admin_header = Helper.get_admin_header()

params200 = "header, expected, ", [("", 401), (good_header, 200)]
params200admin = "header, expected, ", [("", 401), (admin_header, 200)]


@pytest.mark.order(after="test_crud_user")
@pytest.mark.parametrize(*params200)
def test_read_users(header, expected):
    response = client.get(base_url + "users?skip=0&limit=100", headers=header)
    assert response.status_code == expected, response.text
    assert "password" not in response.text


@pytest.mark.order(after="test_read_users")
@pytest.mark.parametrize(*params200)
def test_read_users_with_search(header, expected):
    response = client.get(base_url + "users?skip=0&limit=100&user_search=mining", headers=header)
    assert response.status_code == expected, response.text


@pytest.mark.order("second")
def test_crud_user():
    header = admin_header
    json_create = {
        "email": "klement@hofbauer.com",
        "user_role": "NetOps",
        "hashed_password": "string"
    }
    response = client.post(url=base_url + "users", json=json_create, headers=header)
    assert response.status_code == 200, "User created" + response.text
    user_id = json.loads(response.text)["user_id"]

    response = client.get(base_url + f"users/{user_id}", headers=header)
    assert response.status_code == 200, "User detail" + response.text
    assert "klement" in response.text

    updated_json = {
        "user_id": user_id,
        "email": "klement@hofbauer.com",
        "user_role": "Manager",
        "is_active": True
    }
    response = client.put(url=base_url + "users", json=updated_json, headers=header)
    assert response.status_code == 200, "User updated " + response.text

    response = client.put(url=base_url + f"users/{user_id}/passwd?hashed_password=anotherpass", headers=header)
    assert response.status_code == 200, "User pass updated " + response.text

    response = client.delete(url=base_url + f"users/{user_id}", headers=header)
    assert response.status_code == 200, "User deleted " + response.text


@pytest.mark.order(after="test_crud_user")
def test_user_change_password():
    header = admin_header
    user_email = "test_user_change_password@example.com"
    json_create = {
        "email": user_email,
        "user_role": "NetOps",
        "hashed_password":
            "$argon2id$v=19$m=2097152,t=1,p=4$I6TUOqcU4vxfK+Xc+3+P8Q$HnFc2LT6sC47yy/SJk6L56Fsi31wqiCUUClZ8WuX4CQ"
    }
    response = client.post(url=base_url + "users", json=json_create, headers=header)
    user_id = json.loads(response.text)["user_id"]

    new_password = 'newstring'
    new_hash = '$argon2id$v=19$m=2097152,t=1,p=4$j1HKGeOccy6l9H5vrbXWmg$I7kFmSw82dk2GSffhvD5e97253nWJm7CcFgjynIvJLg'
    response = client.put(url=base_url + f"users/{user_id}/passwd?hashed_password={new_hash}", headers=header)
    assert response.status_code == 200, response.text

    user_dict = {
        "username": user_email,
        "password": new_password
    }
    response = client.post(url="login/", json=user_dict)
    assert response.status_code == 200, response.text


@pytest.mark.order(after="test_crud_user")
@pytest.mark.parametrize("header, expected, ", [("", 401), (good_header, 401)])
def test_user_change_password_not_auth(header, expected):
    user_id = Helper.get_user_id()
    new_hash = '$argon2id$v=19$m=2097152,t=1,p=4$j1HKGeOccy6l9H5vrbXWmg$I7kFmSw82dk2GSffhvD5e97253nWJm7CcFgjynIvJLg'
    response = client.put(url=base_url + f"users/{user_id}/passwd?hashed_password={new_hash}", headers=header)
    assert response.status_code == expected, response.text


@pytest.mark.order(after="test_crud_user")
@pytest.mark.parametrize(*params200admin)
def test_user_create(header, expected):
    json_create = {
        "email": "claude@colombiere.fr",
        "user_role": "Superuser",
        "hashed_password": "lfsdkjfal"
    }
    response = client.post(url=base_url + "users", json=json_create, headers=header)
    assert response.status_code == expected, response.text


@pytest.mark.order(after="test_crud_user")
def test_user_create_bad_email():
    json_create = {
        "email": "colombiere.fr",
        "user_role": "Superuser",
        "hashed_password": "lfsdkjfal"
    }
    response = client.post(url=base_url + "users", json=json_create, headers=admin_header)
    assert response.status_code == 422, response.text


@pytest.mark.order(after="test_user_create")
@pytest.mark.parametrize(*params200)
def test_user_view(header, expected):
    user_id = Helper.get_user_id()
    response = client.get(base_url + f"users/{user_id}", headers=header)
    assert response.status_code == expected, response.text
    if expected == 200:
        assert "user_role" in response.text and "email" in response.text
        assert "hashed_password" not in response.text


@pytest.mark.order(after="test_crud_user")
@pytest.mark.parametrize(*params200admin)
def test_user_update(header, expected):
    email = "don@bosco.it"
    response = client.get(base_url + f"users?skip=0&limit=100&user_search={email}", headers=admin_header)
    json_resp = json.loads(response.text)
    if len(json_resp) == 0:
        user_id = Helper.create_user(email, "NetOps", "passstring")
    else:
        user_id = json_resp[0]["user_id"]

    updated_json = {
        "user_id": user_id,
        "email": email,
        "user_role": "Manager",
        "is_active": False
    }
    response = client.put(url=base_url + "users", json=updated_json, headers=header)
    assert response.status_code == expected, response.text


@pytest.mark.order(after="test_crud_user")
@pytest.mark.parametrize(*params200admin)
def test_user_delete_not_present(header, expected):
    response = client.delete(url=base_url + f"users/888888", headers=header)
    assert response.status_code == expected, response.text


@pytest.mark.order(after="test_user_create")
def test_user_list():
    user_id = Helper.get_user_id()
    response = client.get(base_url + f"users/{user_id}", headers=admin_header)
    email: str = json.loads(response.text)["email"]
    header = good_header

    response = client.get(url=base_url + f"users?skip=0&limit=100&user_search={email}", headers=header)
    assert response.status_code == 200  # User list with search
    assert email in response.text
    assert str(user_id) in response.text

    email_part = email[0:3]
    response = client.get(url=base_url + f"users?skip=0&limit=100&user_search={email_part}", headers=header)
    assert response.status_code == 200  # User list with partial search
    assert email_part in response.text

    response = client.get(url=base_url + f"users?skip=-5&limit=100&user_search={email_part}", headers=header)
    assert response.status_code == 422


@pytest.mark.parametrize(*params200)
def test_user_roles(header, expected):
    response = client.get(url=base_url + f"user-roles", headers=header)
    assert response.status_code == expected
    if expected == 200:
        assert '"Support":1,' in response.text


