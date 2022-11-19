import json

from src.test.end_to_end.helper import Helper
from src.test.end_to_end.test_main import client, base_url


def test_read_incidents_empty():
    response = client.get(base_url + "incidents?skip=0&limit=20")
    assert response.status_code == 200, "Empty incidents list"


def test_read_incidents_empty_all_params():
    response = client.get(base_url + "incidents?incident_id=1&incident_status=Reported&reporter_id=1&resolver_id=1&"
                          + "is_opened=true&incident_priority=Low&incident_search=mining&skip=0&limit=20")
    assert response.status_code == 200, "Empty incidents list"


def test_read_non_existing_incident():
    response = client.get(base_url + "incidents/8888888")
    assert response.status_code == 404


def test_crud_incident():
    created_user_id = Helper.get_user_id()

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

    updated_json = {
      "incident_id": incident_created_id,
      "incident_name": "Updated incident name",
      "incident_description": "Updated incident description",
      "incident_status": "Confirmed",
      "incident_priority": "High",
      "resolver_id": Helper.get_second_user_id()
    }
    response = client.put(url=base_url + "incidents", json=updated_json)
    assert response.status_code == 200, "Incident updated " + response.text

    response = client.delete(url=base_url + f"incidents/{incident_created_id}")
    assert response.status_code == 200, "Incident deleted " + response.text


