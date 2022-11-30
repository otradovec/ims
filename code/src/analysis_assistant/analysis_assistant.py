import json
import os
import re
from typing import Any

from src.middle import incidents, comments


class Assistant:
    def __init__(self):
        self.conf = self.load_conf(self.get_conf_lines())

    def load_conf(self, conf):
        base_url = conf["base_Flowmon_url"]
        for action in conf["actions"]:
            action["url"] = base_url + action["url"]
        return conf

    def get_conf_lines(self):
        filename = "conf.json"
        fpath = os.path.join(os.getcwd(), "src", "analysis_assistant", filename)
        with open(fpath, "r") as f:
            lines = f.readlines()
        lines_str = "\n".join(lines)
        return json.loads(lines_str)

    def advice_get(self, incident_id: int, db) -> Any:
        texts = self.get_texts(db, incident_id)
        result = {
            "actions": []
        }
        for action in self.conf["actions"]:
            if self.is_applicable(action, texts):
                result["actions"].append(action)
        return result

    def is_applicable(self, action, texts):
        regex = action["regex"]
        match = re.search(regex, texts)
        return match is not None

    def get_texts(self, db, incident_id) -> str:
        incident = incidents.get_incident(db=db, incident_id=incident_id)
        incident_texts = incident.incident_name + " " + incident.incident_description
        db_comments = comments.comments_list_full(incident_id=incident_id, db=db)
        comments_texts = ""
        for comment in db_comments:
            comments_texts += " " + comment.comment_text
        texts = incident_texts + " " + comments_texts
        return texts



