import json
import pytest

from src.test.end_to_end.helper import Helper
from src.test.end_to_end.test_main import client, base_url

good_header = Helper.get_header_with_token()
params200 = "header, expected, ", [("", 401), (good_header, 200)]


@pytest.mark.order("third")
@pytest.mark.parametrize(*params200)
def test_read_comments_empty(header, expected):
    incident_id = Helper.get_incident_id()
    response = client.get(base_url + f"comments?incident_id={incident_id}", headers=header)
    assert response.status_code == expected, response.text


@pytest.mark.order(before="test_crud_comment")
def test_read_comments_non_existing_incident():
    response = client.get(base_url + "comments?incident_id=888888", headers=good_header)
    assert response.status_code == 400, response.text


@pytest.mark.order(before="test_crud_comment")
def test_create_comment_unauth():
    created_user_id = Helper.get_user_id()
    incident_id = Helper.get_incident_id()

    url = base_url + f"comments?incident_id={incident_id}&author_id={created_user_id}&comment_text=@RayTussen"
    response = client.post(url=url, headers={})
    assert response.status_code == 401, response.text


@pytest.mark.order(before="test_crud_comment")
def test_view_comment_unauth():
    response = client.get(base_url + f"comments/123")
    assert response.status_code == 401, response.text


@pytest.mark.order(before="test_crud_comment")
def test_update_comment_unauth():
    response = client.put(url=base_url + f"comments?comment_id=123&comment_text=@StevenSmith")
    assert response.status_code == 401, response.text


@pytest.mark.order(before="test_crud_comment")
@pytest.mark.parametrize(*params200)
def test_delete_comment_badly(header, expected):
    response = client.delete(url=base_url + f"comments/888888", headers=header)
    assert response.status_code == expected, response.text


@pytest.mark.order("fourth")
def test_crud_comment():
    created_user_id = Helper.get_user_id()
    incident_id = Helper.get_incident_id()
    header = good_header

    url = base_url + f"comments?incident_id={incident_id}&author_id={created_user_id}&comment_text=@RayTussen"
    response = client.post(url=url, headers=header)
    assert response.status_code == 200, response.text  # Comment created
    comment_id = json.loads(response.text)["comment_id"]

    response = client.get(base_url + f"comments/{comment_id}", headers=header)
    assert response.status_code == 200, response.text  # Comment detail
    assert "RayTussen" in response.text

    response = client.put(url=base_url + f"comments?comment_id={comment_id}&comment_text=@StevenSmith", headers=header)
    assert response.status_code == 200, "Comment updated " + response.text

    response = client.get(base_url + f"comments/{comment_id}", headers=header)
    assert response.status_code == 200, response.text  # Comment detail updated
    assert "StevenSmith" in response.text

    response = client.delete(url=base_url + f"comments/{comment_id}", headers=header)
    assert response.status_code == 200, "Comment deleted " + response.text

    response = client.get(base_url + f"comments/{comment_id}", headers=header)
    assert response.status_code == 404, response.text  # Comment detail not present
    assert "StevenSmith" not in response.text


@pytest.mark.order("fourth")
def test_bad_create_comment_request():
    created_user_id = Helper.get_user_id()
    incident_id = Helper.get_incident_id()
    header = good_header

    url_bad_incident_id = base_url + f"comments?incident_id=8888888&author_id={created_user_id}&comment_text=%40RayTussen"
    response = client.post(url=url_bad_incident_id, headers=header)
    assert response.status_code == 400, response.text  # Comment not created

    url_bad_author_id = base_url + f"comments?incident_id={incident_id}&author_id=88888888&comment_text=%40RayTussen"
    response = client.post(url=url_bad_author_id, headers=header)
    assert response.status_code == 400, response.text  # Comment not created

    url_bad_both_ids = base_url + f"comments?incident_id=8888888&author_id=888888&comment_text=%40RayTussen"
    response = client.post(url=url_bad_both_ids, headers=header)
    assert response.status_code == 400, response.text  # Comment not created


@pytest.mark.order("fourth")
def test_list_comments():
    incident_id = Helper.get_incident_id()
    header = good_header
    response = client.get(base_url + f"comments?incident_id={incident_id}", headers=header)
    assert response.status_code == 200, response.text

    response = client.get(base_url + f"comments?incident_id={incident_id}&skip=0&limit=20", headers=header)
    assert response.status_code == 200, response.text

    response = client.get(base_url + f"comments?incident_id={incident_id}&skip=-5&limit=20", headers=header)
    assert response.status_code == 422, response.text

    response = client.get(base_url + f"comments?incident_id={incident_id}&skip=0&limit=-20", headers=header)
    assert response.status_code == 422, response.text


@pytest.mark.order(after="test_read_comments_empty")
def test_updated_comment_after_updated_attachment():
    header = good_header
    comment_id = Helper.get_comment_id()
    response = client.get(base_url + f"comments/{comment_id}", headers=header)
    comment_updated_at_before = json.loads(response.text)["comment_updated_at"]
    Helper.create_attachment(comment_id=comment_id, filename="AnomTestImage.png")
    response = client.get(base_url + f"comments/{comment_id}", headers=header)
    comment_updated_at_after = json.loads(response.text)["comment_updated_at"]
    assert comment_updated_at_before != comment_updated_at_after
