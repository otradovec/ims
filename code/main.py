from typing import Union
from fastapi import Cookie, FastAPI

from middle.Incident import Incident, incident_list
from middle.UserRole import UserRole
from middle.IncidentStatus import IncidentStatus

app = FastAPI()
base_url = "/ims/rest/"
connected_events_tag = "Connected Events"
comments_tag = "Comments"
users_tag = "Users"
incident_tag = "Incidents"


@app.get(base_url + "incidents", tags=[incident_tag])
async def incidents_list(reported_id: Union[int, None] = None, resolver_id: Union[int, None] = None, incident_status: Union[IncidentStatus, None] = None, incident_priority: Union[int, None] = None, is_opened: Union[bool, None] = None, incident_search: Union[str, None] = None):
    return incident_list(reported_id, resolver_id, incident_status, incident_priority, is_opened, incident_search)


@app.post(base_url + "incidents", tags=[incident_tag])
async def incident_create(reported_id: int, resolver_id: int, incident_status: IncidentStatus, incident_name: str, incident_description: str, incident_priority: int):
    return {"message": reported_id}


@app.put(base_url + "incidents", tags=[incident_tag])
async def incident_update(incident_id: int, resolver_id: int, incident_status: IncidentStatus, incident_name: str, incident_description: str, incident_priority: int):
    return {"message": incident_id}


@app.get(base_url + "incidents/{incident_id}", tags=[incident_tag])
async def incident_detail(incident_id: int):
    return {"message": incident_id}


@app.delete(base_url + "incidents/{incident_id}", tags=[incident_tag])
async def incident_delete(incident_id: int):
    return {"message": incident_id}


@app.get(base_url + "incident-states", tags=[incident_tag])
async def incident_states():
    return {"message": "Those are the states"}


@app.get(base_url + "incident-states/{incident_state_id}", tags=[incident_tag])
async def incident_states(incident_state_id: int):
    return {incident_state_id: "The state is"}


@app.get(base_url + "connected-events", tags=[connected_events_tag])
async def connected_events_list(incident_id: Union[int, None] = None, event_id: Union[int, None] = None):
    return {"The ": "The state is"}


@app.post(base_url + "connected-events", tags=[connected_events_tag])
async def connected_events_create(incident_id: int, event_id: int):
    return {"The ": incident_id}


@app.delete(base_url + "connected-events", tags=[connected_events_tag])
async def connected_events_delete(incident_id: int, event_id: int):
    return {"The ": "The state is"}


@app.get(base_url + "comments", tags=[comments_tag])
async def comments_list(incident_id: int):
    return {"The ": incident_id}


@app.post(base_url + "comments", tags=[comments_tag])
async def comment_create(incident_id: int, author_id: int, comment_text: str):
    return {"The ": incident_id}


@app.get(base_url + "comments/{comment_id}", tags=[comments_tag])
async def comment_view(comment_id: int):
    return {"The ": comment_id}


@app.put(base_url + "comments/{comment_id}", tags=[comments_tag])
async def comment_update(comment_id: int, comment_text: str):
    return {"The ": comment_id}


@app.delete(base_url + "comments/{comment_id}", tags=[comments_tag])
async def comment_delete(comment_id: int):
    return {"The ": comment_id}


@app.get(base_url + "attachments", tags=[comments_tag])
async def attachments_list(comment_id: int):
    return {"The ": comment_id}


@app.post(base_url + "attachments", tags=[comments_tag])
async def attachment_create(comment_id: int, attachment_path: str):
    return {"The ": comment_id}


@app.get(base_url + "attachments/{attachment_id}", tags=[comments_tag])
async def attachment_view(attachment_id: int):
    return {"The ": attachment_id}


@app.delete(base_url + "attachments/{attachment_id}", tags=[comments_tag])
async def attachment_delete(attachment_id: int):
    return {"The ": attachment_id}


# Users
@app.get(base_url + "users", tags=[users_tag])
async def users_list(user_search: Union[str, None] = None):
    return {"The ": user_search}


@app.post(base_url + "users", tags=[users_tag])
async def user_create(email: str, user_role: UserRole, password: str):
    return {"The ": email}


@app.get(base_url + "users/{user_id}", tags=[users_tag])
async def user_view(user_id: int):
    return {"The ": user_id}


@app.put(base_url + "users/{user_id}", tags=[users_tag])
async def user_update(user_id: int, email: str, user_role: UserRole, password: str):
    return {"The ": user_id}


@app.delete(base_url + "users/{user_id}", tags=[users_tag])
async def user_delete(user_id: int):
    return {"The ": user_id}


@app.post(base_url + "users/{user_id}/token", tags=[users_tag])
async def user_token(user_id: int, user_session_cookie: str = Cookie(default=None)):
    return {"The ": user_id}