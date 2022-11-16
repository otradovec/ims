from src.test.end_to_end.test_main import client, base_url


def test_read_incidents_empty():
    response = client.get(base_url + "incidents?skip=0&limit=20")
    assert response.status_code == 200, "Empty incidents list"


def test_read_incidents_empty_all_params():
    response = client.get(base_url + "incidents?incident_id=1&incident_status=Reported&reporter_id=1&resolver_id=1&"
                                   + "is_opened=true&incident_priority=Low&incident_search=mining&skip=0&limit=20")
    assert response.status_code == 200, "Empty incidents list"
