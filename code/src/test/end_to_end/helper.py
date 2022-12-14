import json, pytest, os

from src.test.end_to_end.test_main import client, base_url


class Helper:
    userID1 = userID2 = None
    incidentID1 = commentID1 = None
    token = None

    @classmethod
    def get_user_id(cls) -> int:
        if cls.userID1 is None:
            secret_hash = cls.get_secret()["hash"]
            user_id = cls.create_user("test@example.com", "NetOps", secret_hash)
            cls.userID1 = user_id
            return user_id
        else:
            return cls.userID1

    @classmethod
    def create_user(cls, email, role, passwd) -> int:
        json_create = {
            "email": email,
            "user_role": role,
            "hashed_password": passwd
        }
        response = client.post(url=base_url + "users", json=json_create)
        if response.status_code != 200:
            pytest.fail(f" Test Class: {cls.__name__}:: User failed to be created:: " + str(json_create) + response.text)
        response_json = json.loads(response.text)
        return response_json["user_id"]

    @classmethod
    def get_second_user_id(cls) -> int:
        if cls.userID2 is None:
            user_id = cls.create_user("ops@company.org", "Manager", "hardsecretstring")
            cls.userID2 = user_id
            return user_id
        else:
            return cls.userID2

    @classmethod
    def get_incident_id(cls):
        if cls.incidentID1 is None:
            json_create = {
                "incident_name": "Cryptocurrency mining",
                "incident_description": "There is a cryptocurrency mining reported on the main server",
                "incident_status": "Reported",
                "incident_priority": "Medium",
                "reporter_id": cls.get_user_id(),
                "resolver_id": cls.get_second_user_id()
            }
            incident_id = cls.create_incident(json_create)
            cls.incidentID1 = incident_id
            return incident_id
        else:
            return cls.incidentID1

    @classmethod
    def create_incident(cls, json_create):
        response = client.post(url=base_url + "incidents", json=json_create)
        response_json = json.loads(response.text)
        return response_json["incident_id"]

    @classmethod
    def get_comment_id(cls):
        if cls.commentID1 is not None:
            return cls.commentID1
        else:
            author_id = cls.get_user_id()
            incident_id = cls.get_incident_id()
            comment_text = "Mining%20occurs%20every%20night"
            comment_id = cls.create_comment(incident_id, author_id, comment_text)
            cls.commentID1 = comment_id
            return comment_id

    @classmethod
    def create_comment(cls, incident_id, author_id, comment_text) -> int:
        url = base_url + f"comments?incident_id={incident_id}&author_id={author_id}&comment_text={comment_text}"
        response = client.post(url=url, headers=cls.get_header_with_token())
        response_json = json.loads(response.text)
        return response_json["comment_id"]

    @classmethod
    def create_attachment(cls, comment_id, filename):
        fpath = os.path.join(os.getcwd(), "src", "test", filename)
        with open(fpath, "rb") as f:
            response = client.post(base_url + f"attachments?comment_id={comment_id}",
                                   files={"file": (filename, f, "image/jpeg")})
        return response.text

    @classmethod
    def get_token(cls) -> str:
        if cls.token is None:
            assert cls.get_user_id() is not None
            user_dict = {
                "username": "test@example.com",
                "password": cls.get_secret()["password"]
            }
            response = client.post("/token", data=user_dict)
            assert response.status_code == 200, response.text
            response_json = json.loads(response.text)
            cls.token = response_json["access_token"]

        return cls.token

    @classmethod
    def get_header_with_token(cls) -> dict:
        token = cls.get_token()
        return {"Authorization": "Bearer " + token}

    @classmethod
    def get_secret(cls):
        fpath = os.path.join(os.getcwd(), "src", "test", "end_to_end", ".secrets")
        with open(fpath, "r") as f:
            lines = f.readlines()
        lines_str = "\n".join(lines)
        json_secrets = json.loads(lines_str)
        secret = json_secrets["secrets"][0]
        return secret
