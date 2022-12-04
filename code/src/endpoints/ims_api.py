from typing import Union

from fastapi import Depends, FastAPI, HTTPException, UploadFile
from pydantic.types import NonNegativeInt, PositiveInt
from sqlalchemy.orm import Session

from src.analysis_assistant.analysis_assistant import Assistant
from src.middle.UserRole import UserRole
from src.middle.enum_to_json import enum_to_json
from src.middle import comments, connected_events, incidents, users
from src.models import models
from src.schemas import schemas
from src.database.database import engine
from src.endpoints import dependencies
from src.endpoints import incident_endpoints

models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="IMS REST API documentation")
app.include_router(incident_endpoints.app)
connected_events_tag = "Connected Events"
comments_tag = "Comments"
users_tag = "Users"
assistant_tag = "Analysis assistant"
assistant = Assistant()
base_url = dependencies.base_url


@app.get(base_url + "connected-events", tags=[connected_events_tag])
async def connected_events_list(incident_id: Union[NonNegativeInt, None] = None,
                                event_id: Union[NonNegativeInt, None] = None,
                                skip: NonNegativeInt = 0, limit: PositiveInt = 20,
                                db: Session = Depends(dependencies.get_db)):
    return connected_events.connected_events_list(incident_id=incident_id, event_id=event_id, skip=skip, limit=limit,
                                                  db=db)


@app.post(base_url + "connected-events", tags=[connected_events_tag])
async def connected_events_create(connected_event: schemas.ConnectedEvent = Depends(), db: Session = Depends(dependencies.get_db)):
    existing_connections_list = connected_events.connected_events_list(connected_event.incident_id,
                                                                       connected_event.event_id, db)
    if len(existing_connections_list) > 0:
        raise HTTPException(status_code=400, detail="Connection already present")

    incident = incidents.get_incident(db, connected_event.incident_id)
    if incident is None:
        raise HTTPException(status_code=400, detail="No incident with incident_id")

    return connected_events.connected_events_create(connected_event, db)


@app.delete(base_url + "connected-events", tags=[connected_events_tag])
async def connected_events_delete(connected_event: schemas.ConnectedEvent = Depends(), db: Session = Depends(dependencies.get_db)):
    return connected_events.connected_events_delete(connected_event, db)


@app.get(base_url + "comments", tags=[comments_tag])
async def comments_list(incident_id: NonNegativeInt, skip: NonNegativeInt = 0, limit: PositiveInt = 20,
                        db: Session = Depends(dependencies.get_db)):
    incident = incidents.get_incident(db, incident_id)
    if incident is None:
        raise HTTPException(status_code=400, detail="No incident with incident_id")

    return comments.comments_list(incident_id, skip, limit, db)


@app.post(base_url + "comments", tags=[comments_tag])
async def comment_create(comment: schemas.CommentCreate = Depends(), db: Session = Depends(dependencies.get_db)):
    incident = incidents.get_incident(db, comment.incident_id)
    if incident is None:
        raise HTTPException(status_code=400, detail="No incident with incident_id")

    user = users.get_user(db, comment.author_id)
    if user is None:
        raise HTTPException(status_code=400, detail="No user with author_id specified")

    return comments.comment_create(comment, db)


@app.get(base_url + "comments/{comment_id}", tags=[comments_tag])
async def comment_view(comment_id: NonNegativeInt, db: Session = Depends(dependencies.get_db)):
    db_comment = comments.get_comment(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment


@app.put(base_url + "comments", tags=[comments_tag])
async def comment_update(comment_id: NonNegativeInt, comment_text: str, db: Session = Depends(dependencies.get_db)):
    comment_found = db.query(models.Comment).filter(models.Comment.comment_id == comment_id).first()
    if comment_found is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    comments.update_comment(comment_text=comment_text, comment_found=comment_found, db_session=db)
    return "OK"


@app.delete(base_url + "comments/{comment_id}", tags=[comments_tag])
async def comment_delete(comment_id: NonNegativeInt, db: Session = Depends(dependencies.get_db)):
    return comments.comment_delete(comment_id, db)


@app.get(base_url + "attachments", tags=[comments_tag])
async def attachments_list(comment_id: NonNegativeInt, db: Session = Depends(dependencies.get_db)):
    comment = comments.get_comment(db, comment_id)
    if comment is None:
        raise HTTPException(status_code=400, detail="No comment with comment_id specified")

    return comments.attachments_list(comment_id, db)


@app.post(base_url + "attachments", tags=[comments_tag])
async def attachment_create(comment_id: NonNegativeInt, file: UploadFile, db: Session = Depends(dependencies.get_db)):
    comment = comments.get_comment(db, comment_id)
    if comment is None:
        raise HTTPException(status_code=400, detail="No comment with comment_id specified")

    contents = await file.read()
    filename = file.filename
    content_type = file.content_type
    return comments.attachment_create(comment_id, contents, filename, content_type, db)


@app.get(base_url + "attachments/{attachment_id}", tags=[comments_tag])
async def attachment_view(attachment_id: NonNegativeInt, db: Session = Depends(dependencies.get_db)):
    db_attachment = comments.attachment_get(attachment_id=attachment_id, db=db)
    if db_attachment is None:
        raise HTTPException(status_code=404, detail="Attachment not found")
    return db_attachment


@app.delete(base_url + "attachments/{attachment_id}", tags=[comments_tag])
async def attachment_delete(attachment_id: NonNegativeInt, db: Session = Depends(dependencies.get_db)):
    return comments.attachment_delete(attachment_id, db)


@app.get(base_url + "assistant/{incident_id}", tags=[assistant_tag])
async def advice_get(incident_id: NonNegativeInt, db: Session = Depends(dependencies.get_db)):
    db_incident = incidents.get_incident(db=db, incident_id=incident_id)
    if db_incident is None:
        raise HTTPException(status_code=422, detail="Incident not found")
    return assistant.advice_get(incident_id, db)


# Users
@app.get(base_url + "users", tags=[users_tag])
async def users_list(skip: NonNegativeInt = 0, limit: PositiveInt = 20,
                     db: Session = Depends(dependencies.get_db), user_search: Union[str, None] = None):
    db_users = users.get_users(db, skip=skip, limit=limit, user_search=user_search)
    return db_users


@app.post(base_url + "users", tags=[users_tag])
async def user_create(user: schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
    if user.user_role is None:
        raise HTTPException(status_code=422, detail="Role cannot be empty.")
    db_user = users.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return users.create_user(db=db, user=user)


@app.get(base_url + "users/{user_id}", tags=[users_tag])
async def user_view(user_id: NonNegativeInt, db: Session = Depends(dependencies.get_db)):
    db_user = users.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put(base_url + "users", tags=[users_tag])
async def user_update(user_updated: schemas.User, db: Session = Depends(dependencies.get_db)):
    user_found = db.query(models.User).filter(models.User.user_id == user_updated.user_id).first()
    if user_found is None:
        raise HTTPException(status_code=404, detail="User not found")
    users.update_user(user_updated=user_updated, user_found=user_found, db_session=db)
    return user_updated


@app.put(base_url + "users/{user_id}/passwd", tags=[users_tag])
async def user_update_passwd(user_id: NonNegativeInt, hashed_password: str, db: Session = Depends(dependencies.get_db)):
    user_found = db.query(models.User).filter(models.User.user_id == user_id).first()
    if user_found is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user = users.user_update_passwd(user_id=user_id, user_passwd=hashed_password, db_session=db)
    return db_user


@app.delete(base_url + "users/{user_id}", tags=[users_tag])
async def user_delete(user_id: NonNegativeInt, db: Session = Depends(dependencies.get_db)):
    return users.user_delete(user_id, db)


@app.get(base_url + "user-roles", tags=[users_tag])
async def user_roles():
    return enum_to_json(UserRole)


"""
@app.post(base_url + "users/{user_id}/token", tags=[users_tag])
async def user_token(user_id: NonNegativeInt, user_session_cookie: str = Cookie(default=None)):
    return {"The ": user_id}
"""
