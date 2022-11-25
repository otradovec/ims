import pytest, json

from src.test.end_to_end.helper import Helper
from src.test.end_to_end.test_main import client, base_url


@pytest.mark.order("third")
def test_read_comments_empty():
    incident_id = Helper.get_incident_id()
    response = client.get(base_url + f"comments?incident_id={incident_id}")
    assert response.status_code == 200, response.text


@pytest.mark.order("first")
def test_read_comments_non_existing_incident():
    response = client.get(base_url + "comments?incident_id=888888")
    assert response.status_code == 400, response.text


@pytest.mark.order("fourth")
def test_crud_comment():
    created_user_id = Helper.get_user_id()
    incident_id = Helper.get_incident_id()

    response = client.post(url=base_url + f"comments?incident_id={incident_id}&author_id={created_user_id}&comment_text=%40RayTussen")
    assert response.status_code == 200, response.text  # Comment created
    comment_id = json.loads(response.text)["comment_id"]

    response = client.get(base_url + f"comments/{comment_id}")
    assert response.status_code == 200, response.text  # Comment detail
    assert "RayTussen" in response.text

    response = client.put(url=base_url + f"comments?comment_id={comment_id}&comment_text=%40StevenSmith")
    assert response.status_code == 200, "Comment updated " + response.text

    response = client.get(base_url + f"comments/{comment_id}")
    assert response.status_code == 200, response.text  # Comment detail updated
    assert "StevenSmith" in response.text

    response = client.delete(url=base_url + f"comments/{comment_id}")
    assert response.status_code == 200, "Comment deleted " + response.text

    response = client.get(base_url + f"comments/{comment_id}")
    assert response.status_code == 404, response.text  # Comment detail not present
    assert "StevenSmith" not in response.text


@pytest.mark.order("fourth")
def test_bad_create_comment_request():
    created_user_id = Helper.get_user_id()
    incident_id = Helper.get_incident_id()

    response = client.post(url=base_url + f"comments?incident_id=8888888&author_id={created_user_id}&comment_text=%40RayTussen")
    assert response.status_code == 400, response.text  # Comment not created

    response = client.post(url=base_url + f"comments?incident_id={incident_id}&author_id=88888888&comment_text=%40RayTussen")
    assert response.status_code == 400, response.text  # Comment not created

    response = client.post(url=base_url + f"comments?incident_id=8888888&author_id=888888&comment_text=%40RayTussen")
    assert response.status_code == 400, response.text  # Comment not created


@pytest.mark.order("fourth")
def test_list_comments():
    incident_id = Helper.get_incident_id()
    response = client.get(base_url + f"comments?incident_id={incident_id}")
    assert response.status_code == 200, response.text

    response = client.get(base_url + f"comments?incident_id={incident_id}&skip=0&limit=20")
    assert response.status_code == 200, response.text

