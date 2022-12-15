import json
import pytest

from src.test.end_to_end.helper import Helper
from src.test.end_to_end.test_main import client, base_url

good_header = Helper.get_header_with_token()

params200 = "header, expected, ", [("", 401), (good_header, 200)]
params404 = "header, expected, ", [("", 401), (good_header, 404)]


@pytest.mark.order("first")
@pytest.mark.parametrize(*params200)
def test_read_incidents_empty(header, expected):
    response = client.get(base_url + "incidents?skip=0&limit=20", headers=header)
    assert response.status_code == expected, "Empty incidents list"


@pytest.mark.order("first")
@pytest.mark.parametrize(*params200)
def test_read_incidents_empty_all_params(header, expected):
    url = base_url + "incidents?incident_id=1&incident_status=Reported&reporter_id=1&resolver_id=1&is_opened=true" \
                     "&incident_priority=Low&incident_search=mining&skip=0&limit=20 "
    response = client.get(url=url, headers=header)
    assert response.status_code == expected, "Empty incidents list"


@pytest.mark.order("first")
@pytest.mark.parametrize(*params404)
def test_read_non_existing_incident(header, expected):
    response = client.get(base_url + "incidents/8888888", headers=header)
    assert response.status_code == expected


def test_create_incident_unauth():
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
    assert response.status_code == 401, response.text  # Incident not created


@pytest.mark.order(after="test_crud_incident")
def test_view_incident_unauth():
    incident_id = Helper.get_incident_id()
    response = client.get(base_url + f"incidents/{incident_id}")
    assert response.status_code == 401, response.text


@pytest.mark.order(after="test_crud_incident")
def test_update_incident_unauth():
    updated_json = {
        "incident_id": Helper.get_incident_id(),
        "incident_name": "Updated incident name",
        "incident_description": "Updated incident description",
        "incident_status": "Confirmed",
        "incident_priority": "High",
        "resolver_id": Helper.get_second_user_id()
    }
    response = client.put(url=base_url + "incidents", json=updated_json)
    assert response.status_code == 401, response.text


@pytest.mark.order(after="test_crud_incident")
def test_delete_incident_not_present():
    response = client.delete(url=base_url + f"incidents/8888888888", headers=good_header)
    assert response.status_code == 200, response.text


@pytest.mark.order(after="test_crud_incident")
def test_delete_incident_unauth():
    incident_id = Helper.get_incident_id()
    response = client.delete(url=base_url + f"incidents/{incident_id}")
    assert response.status_code == 401, response.text


def test_crud_incident():
    created_user_id = Helper.get_user_id()
    header = good_header

    json_create = {
        "incident_name": "Cryptocurrency mining",
        "incident_description": "There is a cryptocurrency mining reported on the main server",
        "incident_status": "Reported",
        "incident_priority": "Medium",
        "reporter_id": created_user_id,
        "resolver_id": created_user_id
    }
    response = client.post(url=base_url + "incidents", json=json_create, headers=header)
    assert response.status_code == 200, response.text  # Incident created
    incident_created_id = json.loads(response.text)["incident_id"]

    response = client.get(base_url + f"incidents/{incident_created_id}", headers=header)
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
    response = client.put(url=base_url + "incidents", json=updated_json, headers=header)
    assert response.status_code == 200, "Incident updated " + response.text

    response = client.delete(url=base_url + f"incidents/{incident_created_id}", headers=header)
    assert response.status_code == 200, "Incident deleted " + response.text


@pytest.mark.parametrize(*params200)
def test_incident_states(header, expected):
    response = client.get(url=base_url + f"incident-states", headers=header)
    assert response.status_code == expected, response.text
    if expected == 200:
        assert "Reported" in response.text


@pytest.mark.parametrize(*params200)
def test_incident_priorities(header, expected):
    response = client.get(url=base_url + f"incident-priorities", headers=header)
    assert response.status_code == expected, response.text
    if expected == 200:
        assert "Medium" in response.text


@pytest.mark.order(after="test_attachments.py::test_read_attachments_empty")
def test_incident_updated_after_changed_comment_text():
    comment_id = Helper.get_comment_id()
    header = good_header
    response = client.get(base_url + f"comments/{comment_id}", headers=header)
    incident_id = json.loads(response.text)["incident_id"]

    response = client.get(base_url + f"incidents/{incident_id}", headers=header)
    incident_updated_at_before = json.loads(response.text)["incident_updated_at"]

    client.put(url=base_url + f"comments?comment_id={comment_id}&comment_text=%40Jacob", headers=header)

    response = client.get(base_url + f"incidents/{incident_id}", headers=header)
    incident_updated_at_after = json.loads(response.text)["incident_updated_at"]

    assert incident_updated_at_before != incident_updated_at_after


@pytest.mark.order(after="test_read_attachments_empty")
def test_incident_updated_after_changed_comment_attachment():
    comment_id = Helper.get_comment_id()
    header = good_header
    response = client.get(base_url + f"comments/{comment_id}", headers=header)
    incident_id = json.loads(response.text)["incident_id"]

    response = client.get(base_url + f"incidents/{incident_id}", headers=header)
    incident_updated_at_before = json.loads(response.text)["incident_updated_at"]

    Helper.create_attachment(comment_id=comment_id, filename="AnomTestImage.png")

    response = client.get(base_url + f"incidents/{incident_id}", headers=header)
    incident_updated_at_after = json.loads(response.text)["incident_updated_at"]

    assert incident_updated_at_before != incident_updated_at_after
