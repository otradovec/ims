import pytest, os, json

from src.test.end_to_end.helper import Helper
from src.test.end_to_end.test_main import client, base_url

good_header = Helper.get_header_with_token()
params200 = "header, expected, ", [("", 401), (good_header, 200)]


@pytest.mark.order(after='test_comments.py::test_crud_comment')
@pytest.mark.parametrize(*params200)
def test_read_attachments_empty(header, expected):
    comment_id = Helper.get_comment_id()
    response = client.get(base_url + f"attachments?comment_id={comment_id}", headers=header)
    assert response.status_code == expected, response.text


@pytest.mark.order(after="test_crd_attachment")
def test_create_attachment_unauth():
    comment_id = Helper.get_comment_id()
    filename = "AnomTestImage.png"
    fpath = os.path.join(os.getcwd(), "src", "test", filename)
    with open(fpath, "rb") as f:
        response = client.post(base_url + f"attachments?comment_id={comment_id}",
                               files={"file": (filename, f, "image/jpeg")})
    assert response.status_code == 401


@pytest.mark.order(after="test_crd_attachment")
@pytest.mark.parametrize("header, expected, ", [("", 401), (good_header, 404)])
def test_read_attachment_badly(header, expected):
    response = client.get(base_url + f"attachments/8888888", headers=header)
    assert response.status_code == expected, response.text


@pytest.mark.order(after="test_crd_attachment")
@pytest.mark.parametrize(*params200)
def test_delete_attachment_badly(header, expected):
    response = client.delete(base_url + f"attachments/8888888", headers=header)
    assert response.status_code == expected, response.text


@pytest.mark.order("fifth")
def test_crd_attachment():
    header = good_header
    comment_id = Helper.get_comment_id()
    filename = "AnomTestImage.png"
    fpath = os.path.join(os.getcwd(), "src", "test", filename)
    with open(fpath, "rb") as f:
        url = base_url + f"attachments?comment_id={comment_id}"
        response = client.post(url=url, files={"file": (filename, f, "image/jpeg")}, headers=header)
    assert response.status_code == 200, response.text  # Created attachment
    attachment_id = json.loads(response.text)["attachment_id"]

    response = client.get(base_url + f"attachments?comment_id={comment_id}", headers=header)
    assert response.status_code == 200, response.text  # Get attachments
    assert filename in response.text

    response = client.get(base_url + f"attachments/{attachment_id}", headers=header)
    assert response.status_code == 200, response.text  # Get attachment

    response = client.delete(base_url + f"attachments/{attachment_id}", headers=header)
    assert response.status_code == 200, response.text  # Delete attachment

    response = client.get(base_url + f"attachments/{attachment_id}", headers=header)
    assert response.status_code == 404, response.text  # Get deleted attachment
