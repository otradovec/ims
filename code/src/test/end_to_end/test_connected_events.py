import pytest

from src.test.end_to_end.helper import Helper
from src.test.end_to_end.test_main import client, base_url

token_header = Helper.get_header_with_token()


def test_read_connected_events_unauthorized():
    response = client.get(base_url + "connected-events")
    assert response.status_code == 401, response.text


@pytest.mark.order("first")
def test_read_connected_events_empty():
    response = client.get(base_url + "connected-events", headers=token_header)
    assert response.status_code == 200, response.text

    response = client.get(base_url + "connected-events?incident_id=1&event_id=20456", headers=token_header)
    assert response.status_code == 200, "Empty connected events list"

    response = client.get(base_url + "connected-events?event_id=20456", headers=token_header)
    assert response.status_code == 200, "Empty connected events list"

    response = client.get(base_url + "connected-events?incident_id=1", headers=token_header)
    assert response.status_code == 200, "Empty connected events list"


def test_connected_events_create_unauthorized():
    response = client.post(url=base_url + f"connected-events?incident_id=1&event_id=1")
    assert response.status_code == 401, response.text


def test_connected_events_read_unauthorized():
    response = client.get(url=base_url + f"connected-events?incident_id=1&event_id=1")
    assert response.status_code == 401, response.text


def test_connected_events_delete_unauthorized():
    response = client.delete(url=base_url + f"connected-events?incident_id=1&event_id=1")
    assert response.status_code == 401, response.text


def test_connected_events_delete_not_present():
    response = client.delete(url=base_url + f"connected-events?incident_id=888888&event_id=88888", headers=token_header)
    assert response.status_code == 200, response.text


def test_basic_connected_events_crd():
    incident_id = Helper.get_incident_id()
    event_id = 20455
    url = base_url + f"connected-events?incident_id={incident_id}&event_id={event_id}"
    response = client.post(url=url, headers=token_header)
    assert response.status_code == 200, response.text  # Connection created

    response = client.get(url=url, headers=token_header)
    assert response.status_code == 200, response.text  # Connection detail

    response = client.delete(url=url, headers=token_header)
    assert response.status_code == 200, response.text


def test_create_with_bad_ids():
    incident_id = Helper.get_incident_id()
    event_id = 30456
    url = base_url + f"connected-events?incident_id={incident_id}&event_id={event_id}"
    client.post(url=url, headers=token_header)
    response = client.post(url=url, headers=token_header)  # The same request - already existing
    assert response.status_code == 400, response.text

    non_existing_incident_id = 88888
    response = client.post(url=base_url + f"connected-events?incident_id={non_existing_incident_id}&event_id={event_id}",
                           headers=token_header)
    assert response.status_code == 400, response.text
