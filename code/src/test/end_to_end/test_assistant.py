import pytest

from src.test.end_to_end.helper import Helper
from src.test.end_to_end.test_main import client, base_url

token = Helper.get_token()
token_header = {"Authorization": "Bearer " + token}


@pytest.mark.order("first")
def test_read_advices_unauthorized():
    response = client.get(base_url + f"assistant/8888888")
    assert response.status_code == 401, response.text


@pytest.mark.order("first")
def test_read_advices_non_existing_id():
    response = client.get(base_url + f"assistant/8888888", headers=token_header)
    assert response.status_code == 422, response.text


@pytest.mark.order("first")
def test_read_advices_negative_id():
    response = client.get(base_url + f"assistant/-8888888", headers=token_header)
    assert response.status_code == 422, response.text


@pytest.mark.order(after="test_crd_attachment")
def test_read_advices():
    incident_id = Helper.get_incident_id()
    response = client.get(base_url + f"assistant/{incident_id}", headers=token_header)
    assert response.status_code == 200, response.text


@pytest.mark.order(after="test_crd_attachment")
def test_read_advices_voip():
    incident_json = {
        "incident_name": "Unexpected VoIP",
        "incident_description": "There is unexpected VoIP flow. Such activity could be considered as legitimate "
                                "depending on devices and services involved.",
        "incident_priority": "Medium",
        "reporter_id": Helper.get_user_id(),
        "resolver_id": Helper.get_second_user_id()
    }
    incident_id = Helper.create_incident(incident_json)
    response = client.get(base_url + f"assistant/{incident_id}", headers=token_header)
    assert response.status_code == 200, response.text
    assert "VoIP" in response.text
    assert "https://demo.flowmon.com/fmc/voip/" in response.text
