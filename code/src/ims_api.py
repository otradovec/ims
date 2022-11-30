from typing import Union, Optional

from fastapi import Depends, FastAPI, HTTPException, UploadFile
from pydantic.types import NonNegativeInt, PositiveInt
from sqlalchemy.orm import Session

from src.analysis_assistant.analysis_assistant import Assistant
from src.middle.IncidentPriority import IncidentPriority
from src.middle.IncidentStatus import IncidentStatus
from src.middle.UserRole import UserRole
from src.middle.enum_to_json import enum_to_json
from src.middle import comments, connected_events, incidents, users
from src.models import models
from src.schemas import schemas
from src.database.database import SessionLocal, engine

models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
base_url = "/ims/rest/"
connected_events_tag = "Connected Events"
comments_tag = "Comments"
users_tag = "Users"
incident_tag = "Incidents"
assistant_tag = "Analysis assistant"
assistant = Assistant()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get(base_url + "incidents", tags=[incident_tag])
async def incidents_list(incident_status: IncidentStatus = None, reporter_id: int = None,
                         resolver_id: int = None, is_opened: Optional[bool] = None,
                         incident_priority: IncidentPriority = None,
                         incident_search: Optional[str] = None, skip: NonNegativeInt = 0,
                         limit: PositiveInt = 20, db: Session = Depends(get_db)
                         ):
    return incidents.incident_list(incident_status, reporter_id, resolver_id, is_opened, incident_priority,
                                   incident_search, skip, limit, db)


@app.post(base_url + "incidents", tags=[incident_tag])
async def incident_create(incident: schemas.IncidentBase, db: Session = Depends(get_db)):
    db_reporter = users.get_user(db=db, user_id=incident.reporter_id)
    if db_reporter is None:
        raise HTTPException(status_code=400, detail="Reporter not existing")

    db_resolver = users.get_user(db=db, user_id=incident.resolver_id)
    if db_resolver is None:
        raise HTTPException(status_code=400, detail="Resolver not existing")
    return incidents.create_incident(db=db, incident=incident)


@app.put(base_url + "incidents", tags=[incident_tag])
async def incident_update(incident_updated: schemas.IncidentUpdate, db: Session = Depends(get_db)):
    incident_found = db.query(models.Incident).filter(
        models.Incident.incident_id == incident_updated.incident_id).first()
    if incident_found is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    resolver_found = db.query(models.User).filter(models.User.user_id == incident_updated.resolver_id).first()
    if resolver_found is None:
        raise HTTPException(status_code=404, detail="Resolver not found")
    incidents.update_incident(incident_updated=incident_updated, incident_found=incident_found, db_session=db)
    return incident_updated


@app.get(base_url + "incidents/{incident_id}", tags=[incident_tag])
async def incident_detail(incident_id: int, db: Session = Depends(get_db)):
    db_incident = incidents.get_incident(db, incident_id=incident_id)
    if db_incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return db_incident


@app.delete(base_url + "incidents/{incident_id}", tags=[incident_tag])
async def incident_delete(incident_id: int, db: Session = Depends(get_db)):
    return incidents.incident_delete(incident_id, db)


@app.get(base_url + "incident-states", tags=[incident_tag])
async def incident_states():
    return enum_to_json(IncidentStatus)


@app.get(base_url + "incident-priorities", tags=[incident_tag])
async def incident_priorities():
    return enum_to_json(IncidentPriority)


@app.get(base_url + "connected-events", tags=[connected_events_tag])
async def connected_events_list(incident_id: Union[int, None] = None, event_id: Union[int, None] = None,
                                skip: NonNegativeInt = 0, limit: PositiveInt = 20,
                                db: Session = Depends(get_db)):
    return connected_events.connected_events_list(incident_id=incident_id, event_id=event_id, skip=skip, limit=limit,
                                                  db=db)


@app.post(base_url + "connected-events", tags=[connected_events_tag])
async def connected_events_create(incident_id: int, event_id: int, db: Session = Depends(get_db)):
    existing_connections_list = connected_events.connected_events_list(incident_id, event_id, db)
    if len(existing_connections_list) > 0:
        raise HTTPException(status_code=400, detail="Connection already present")

    incident = incidents.get_incident(db, incident_id)
    if incident is None:
        raise HTTPException(status_code=400, detail="No incident with incident_id")

    return connected_events.connected_events_create(incident_id, event_id, db)


@app.delete(base_url + "connected-events", tags=[connected_events_tag])
async def connected_events_delete(incident_id: int, event_id: int, db: Session = Depends(get_db)):
    return connected_events.connected_events_delete(incident_id, event_id, db)


@app.get(base_url + "comments", tags=[comments_tag])
async def comments_list(incident_id: int, skip: NonNegativeInt = 0, limit: PositiveInt = 20,
                        db: Session = Depends(get_db)):
    incident = incidents.get_incident(db, incident_id)
    if incident is None:
        raise HTTPException(status_code=400, detail="No incident with incident_id")

    return comments.comments_list(incident_id, skip, limit, db)


@app.post(base_url + "comments", tags=[comments_tag])
async def comment_create(incident_id: int, author_id: int, comment_text: str, db: Session = Depends(get_db)):
    incident = incidents.get_incident(db, incident_id)
    if incident is None:
        raise HTTPException(status_code=400, detail="No incident with incident_id")

    user = users.get_user(db, author_id)
    if user is None:
        raise HTTPException(status_code=400, detail="No user with author_id specified")

    return comments.comment_create(incident_id, author_id, comment_text, db)


@app.get(base_url + "comments/{comment_id}", tags=[comments_tag])
async def comment_view(comment_id: int, db: Session = Depends(get_db)):
    db_comment = comments.get_comment(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment


@app.put(base_url + "comments", tags=[comments_tag])
async def comment_update(comment_id: int, comment_text: str, db: Session = Depends(get_db)):
    comment_found = db.query(models.Comment).filter(models.Comment.comment_id == comment_id).first()
    if comment_found is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    comments.update_comment(comment_text=comment_text, comment_found=comment_found, db_session=db)
    return "OK"


@app.delete(base_url + "comments/{comment_id}", tags=[comments_tag])
async def comment_delete(comment_id: int, db: Session = Depends(get_db)):
    return comments.comment_delete(comment_id, db)


@app.get(base_url + "attachments", tags=[comments_tag])
async def attachments_list(comment_id: int, db: Session = Depends(get_db)):
    comment = comments.get_comment(db, comment_id)
    if comment is None:
        raise HTTPException(status_code=400, detail="No comment with comment_id specified")

    return comments.attachments_list(comment_id, db)


@app.post(base_url + "attachments", tags=[comments_tag])
async def attachment_create(comment_id: int, file: UploadFile, db: Session = Depends(get_db)):
    comment = comments.get_comment(db, comment_id)
    if comment is None:
        raise HTTPException(status_code=400, detail="No comment with comment_id specified")

    contents = await file.read()
    filename = file.filename
    content_type = file.content_type
    return comments.attachment_create(comment_id, contents, filename, content_type, db)


@app.get(base_url + "attachments/{attachment_id}", tags=[comments_tag])
async def attachment_view(attachment_id: int, db: Session = Depends(get_db)):
    db_attachment = comments.attachment_get(attachment_id=attachment_id, db=db)
    if db_attachment is None:
        raise HTTPException(status_code=404, detail="Attachment not found")
    return db_attachment


@app.delete(base_url + "attachments/{attachment_id}", tags=[comments_tag])
async def attachment_delete(attachment_id: int, db: Session = Depends(get_db)):
    return comments.attachment_delete(attachment_id, db)


@app.get(base_url + "assistant/{incident_id}", tags=[assistant_tag])
async def advice_get(incident_id: NonNegativeInt, db: Session = Depends(get_db)):
    db_incident = incidents.get_incident(db=db, incident_id=incident_id)
    if db_incident is None:
        raise HTTPException(status_code=422, detail="Incident not found")
    return assistant.advice_get(incident_id, db)


# Users
@app.get(base_url + "users", tags=[users_tag])
async def users_list(skip: NonNegativeInt = 0, limit: PositiveInt = 20,
                     db: Session = Depends(get_db), user_search: Union[str, None] = None):
    db_users = users.get_users(db, skip=skip, limit=limit, user_search=user_search)
    return db_users


@app.post(base_url + "users", tags=[users_tag])
async def user_create(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if user.user_role is None:
        raise HTTPException(status_code=422, detail="Role cannot be empty.")
    db_user = users.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return users.create_user(db=db, user=user)


@app.get(base_url + "users/{user_id}", tags=[users_tag])
async def user_view(user_id: int, db: Session = Depends(get_db)):
    db_user = users.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put(base_url + "users", tags=[users_tag])
async def user_update(user_updated: schemas.User, db: Session = Depends(get_db)):
    user_found = db.query(models.User).filter(models.User.user_id == user_updated.user_id).first()
    if user_found is None:
        raise HTTPException(status_code=404, detail="User not found")
    users.update_user(user_updated=user_updated, user_found=user_found, db_session=db)
    return user_updated


@app.put(base_url + "users/{user_id}/passwd", tags=[users_tag])
async def user_update_passwd(user_id: int, hashed_password: str, db: Session = Depends(get_db)):
    user_found = db.query(models.User).filter(models.User.user_id == user_id).first()
    if user_found is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user = users.user_update_passwd(user_id=user_id, user_passwd=hashed_password, db_session=db)
    return db_user


@app.delete(base_url + "users/{user_id}", tags=[users_tag])
async def user_delete(user_id: int, db: Session = Depends(get_db)):
    return users.user_delete(user_id, db)


@app.get(base_url + "user-roles", tags=[users_tag])
async def user_roles():
    return enum_to_json(UserRole)


"""
@app.post(base_url + "users/{user_id}/token", tags=[users_tag])
async def user_token(user_id: int, user_session_cookie: str = Cookie(default=None)):
    return {"The ": user_id}
"""
