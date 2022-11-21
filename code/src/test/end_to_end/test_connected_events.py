import pytest

from src.test.end_to_end.helper import Helper
from src.test.end_to_end.test_main import client, base_url


@pytest.mark.order("first")
def test_read_connected_events_empty():
    response = client.get(base_url + "connected-events")
    assert response.status_code == 200, response.text

    response = client.get(base_url + "connected-events?incident_id=1&event_id=20456")
    assert response.status_code == 200, "Empty connected events list"

    response = client.get(base_url + "connected-events?event_id=20456")
    assert response.status_code == 200, "Empty connected events list"

    response = client.get(base_url + "connected-events?incident_id=1")
    assert response.status_code == 200, "Empty connected events list"


def test_basic_connected_events_crd():
    incident_id = Helper.get_incident_id()
    event_id = 20455
    response = client.post(url=base_url + f"connected-events?incident_id={incident_id}&event_id={event_id}")
    assert response.status_code == 200, response.text  # Connection created

    response = client.get(base_url + f"connected-events?incident_id={incident_id}&event_id={event_id}")
    assert response.status_code == 200, response.text  # Connection detail

    response = client.delete(url=base_url + f"connected-events?incident_id={incident_id}&event_id={event_id}")
    assert response.status_code == 200, response.text


def test_create_with_bad_ids():
    incident_id = Helper.get_incident_id()
    event_id = 30456
    url = base_url + f"connected-events?incident_id={incident_id}&event_id={event_id}"
    client.post(url=url)
    response = client.post(url=url)  # The same request - already existing
    assert response.status_code == 400, response.text

    non_existing_incident_id = 88888
    response = client.post(url=base_url + f"connected-events?incident_id={non_existing_incident_id}&event_id={event_id}")
    assert response.status_code == 400, response.text