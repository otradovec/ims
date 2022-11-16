from typing import Union, Optional

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from src.middle.IncidentPriority import IncidentPriority
from src.middle.IncidentStatus import IncidentStatus
from src.models import models
from src.database import crud
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


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

"""


@app.get(base_url + "incidents", tags=[incident_tag], response_model=list[schemas.IncidentFull])
async def incidents_list(incident_id: int = None, incident_status: IncidentStatus = None, reporter_id: int = None,
                         resolver_id: int = None, is_opened: Optional[bool] = None, incident_priority: IncidentPriority = None,
                         incident_search: Optional[str] = None,
                         skip: int = 0, limit: int = 20, db: Session = Depends(get_db)
                         ):
    return crud.incident_list(incident_id, incident_status, reporter_id, resolver_id, is_opened, incident_priority, incident_search, skip, limit, db)


@app.post(base_url + "incidents", tags=[incident_tag])
async def incident_create(incident: schemas.IncidentBase, db: Session = Depends(get_db)):
    db_reporter = crud.get_user(db=db, user_id=incident.reporter_id)
    if db_reporter is None:
        raise HTTPException(status_code=400, detail="Reporter not existing")

    db_resolver = crud.get_user(db=db, user_id=incident.resolver_id)
    if db_resolver is None:
        raise HTTPException(status_code=400, detail="Resolver not existing")
    return crud.create_incident(db=db, incident=incident)


@app.put(base_url + "incidents", tags=[incident_tag])
async def incident_update(incident_id: int, resolver_id: int, incident_status: IncidentStatus, incident_name: str,
                          incident_description: str, incident_priority: int, db: Session = Depends(get_db)):
    return {"message": incident_id}


@app.get(base_url + "incidents/{incident_id}", tags=[incident_tag])
async def incident_detail(incident_id: int, db: Session = Depends(get_db)):
    db_incident = crud.get_incident(db, incident_id=incident_id)
    if db_incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return db_incident


@app.delete(base_url + "incidents/{incident_id}", tags=[incident_tag])
async def incident_delete(incident_id: int, db: Session = Depends(get_db)):
    return {"message": incident_id}


@app.get(base_url + "incident-states", tags=[incident_tag])
async def incident_states():
    return {"message": "Those are the states"}


@app.get(base_url + "incident-states/{incident_state_id}", tags=[incident_tag])
async def incident_states(incident_state_id: int):
    return {incident_state_id: "The state is"}


"""
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

"""


# Users
@app.get(base_url + "users", tags=[users_tag], response_model=list[schemas.User])
async def users_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                     user_search: Union[str, None] = None):
    users = crud.get_users(db, skip=skip, limit=limit, user_search=user_search)
    return users


@app.post(base_url + "users", tags=[users_tag], response_model=schemas.User)
async def user_create(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if user.user_role is None:
        raise HTTPException(status_code=422, detail="Role cannot be empty.")
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get(base_url + "users/{user_id}", tags=[users_tag], response_model=schemas.User)
async def user_view(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put(base_url + "users", tags=[users_tag], response_model=schemas.User)
async def user_update(user_updated: schemas.User, db: Session = Depends(get_db)):
    user_found = db.query(models.User).filter(models.User.user_id == user_updated.user_id).first()
    if user_found is None:
        raise HTTPException(status_code=404, detail="User not found")
    crud.update_user(user_updated=user_updated, user_found=user_found, db_session=db)
    return user_updated


@app.put(base_url + "users/{user_id}/passwd", tags=[users_tag])
async def user_update_passwd(user_id: int, hashed_password: str, db: Session = Depends(get_db)):
    user_found = db.query(models.User).filter(models.User.user_id == user_id).first()
    if user_found is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user = crud.user_update_passwd(user_id=user_id, user_passwd=hashed_password, db_session=db)
    return db_user


@app.delete(base_url + "users/{user_id}", tags=[users_tag])
async def user_delete(user_id: int, db: Session = Depends(get_db)):
    return crud.user_delete(user_id, db)


"""
@app.post(base_url + "users/{user_id}/token", tags=[users_tag])
async def user_token(user_id: int, user_session_cookie: str = Cookie(default=None)):
    return {"The ": user_id}
"""
