import pytest, os, json

from src.test.end_to_end.helper import Helper
from src.test.end_to_end.test_main import client, base_url


@pytest.mark.order("fourth")
def test_read_attachments_empty():
    comment_id = Helper.get_comment_id()
    response = client.get(base_url + f"attachments?comment_id={comment_id}")
    assert response.status_code == 200, response.text


@pytest.mark.order("fifth")
def test_crd_attachment():
    comment_id = Helper.get_comment_id()
    filename = "AnomTestImage.png"
    fpath = os.path.join(os.getcwd(), "src", "test", filename)
    with open(fpath, "rb") as f:
        response = client.post(base_url + f"attachments?comment_id={comment_id}", files={"file": (filename, f, "image/jpeg")})
    assert response.status_code == 200, response.text  # Created attachment
    attachment_id = json.loads(response.text)["attachment_id"]

    response = client.get(base_url + f"attachments?comment_id={comment_id}")
    assert response.status_code == 200, response.text  # Get attachments
    assert filename in response.text

    response = client.get(base_url + f"attachments/{attachment_id}")
    assert response.status_code == 200, response.text  # Get attachment

    response = client.delete(base_url + f"attachments/{attachment_id}")
    assert response.status_code == 200, response.text  # Delete attachment

    response = client.get(base_url + f"attachments/{attachment_id}")
    assert response.status_code == 404, response.text  # Get deleted attachment
