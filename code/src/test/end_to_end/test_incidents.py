import json

from src.test.end_to_end.test_main import client, base_url


def test_read_incidents_empty():
    response = client.get(base_url + "incidents?skip=0&limit=20")
    assert response.status_code == 200, "Empty incidents list"


def test_read_incidents_empty_all_params():
    response = client.get(base_url + "incidents?incident_id=1&incident_status=Reported&reporter_id=1&resolver_id=1&"
                          + "is_opened=true&incident_priority=Low&incident_search=mining&skip=0&limit=20")
    assert response.status_code == 200, "Empty incidents list"


def test_crud_incident():
    created_user_id = get_user_id()
    response = client.get(base_url + "incidents/1")
    assert response.status_code == 404  # Incident not yet created
    json_create = {
        "incident_name": "Cryptocurrency mining",
        "incident_description": "There is a cryptocurrency mining reported on the main server",
        "incident_status": "Reported",
        "incident_priority": "Medium",
        "reporter_id": created_user_id,
        "resolver_id": created_user_id
    }
    response = client.post(url=base_url + "incidents", json=json_create)
    assert response.status_code == 200, response.text  # Incident created
    incident_created_id = json.loads(response.text)["incident_id"]

    response = client.get(base_url + f"incidents/{incident_created_id}")
    assert response.status_code == 200, response.text  # Incident detail
    assert "mining" in response.text


def get_user_id() -> int:
    json_create = {
        "email": "test@user.com",
        "user_role": 2,
        "hashed_password": "secretstring"
    }
    response = client.post(url=base_url + "users", json=json_create)
    response_json = json.loads(response.text)
    return response_json["user_id"]
