import json

from src.test.end_to_end.test_main import client, base_url


class Helper:

    userID1 = userID2 = None
    incidentID1 = None

    @classmethod
    def get_user_id(cls) -> int:
        if cls.userID1 is None:
            user_id = cls.create_user("test@user.com", 2, "secretstring")
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
        response_json = json.loads(response.text)
        return response_json["user_id"]

    @classmethod
    def get_second_user_id(cls) -> int:
        if cls.userID2 is None:
            user_id = cls.create_user("ops@company.org", 3, "hardsecretstring")
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
