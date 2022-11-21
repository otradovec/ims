import datetime

from sqlalchemy.orm import Session, load_only

from src.middle import IncidentStatus
from src.models import models
from src.schemas import schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100, user_search: str = None):
    query = db.query(models.User).offset(skip).limit(limit).options(
        load_only(models.User.user_id, models.User.email, models.User.is_active, models.User.user_role))
    if user_search is None:
        return query.all()
    else:
        return query.filter(models.User.email.like('%' + user_search + '%')).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.hashed_password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password, user_role=user.user_role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(user_updated: schemas.User, user_found: schemas.User, db_session: Session):
    user_id = user_found.user_id
    result = db_session.query(models.User).filter(models.User.user_id == user_id).update({
        "user_id": user_found.user_id,
        "email": user_updated.email,
        "user_role": user_updated.user_role,
        "is_active": user_updated.is_active
    })
    db_session.commit()
    return result


def user_update_passwd(user_id, user_passwd, db_session):
    fake_hashed_password = user_passwd + "notreallyhashed"
    result = db_session.query(models.User).filter(models.User.user_id == user_id).update({
        "hashed_password": fake_hashed_password,
    })
    db_session.commit()
    return result


def user_delete(user_id, db):
    res = db.query(models.User).filter(models.User.user_id == user_id).delete()
    db.commit()
    return res


"""
def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
"""


def incident_list(incident_id, incident_status, reporter_id, resolver_id, is_opened, incident_priority, incident_search,
                  skip, limit, db):
    query = db.query(models.Incident)
    if incident_id is not None:
        query = query.filter(models.Incident.incident_id == incident_id)

    if incident_status is not None:
        status_int = int(incident_status)
        query = query.filter(models.Incident.incident_status == status_int)

    if reporter_id is not None:
        query = query.filter(models.Incident.reporter_id == reporter_id)

    if resolver_id is not None:
        query = query.filter(models.Incident.resolver_id == resolver_id)

    if is_opened is not None:
        query = query.filter(models.Incident.is_opened == is_opened)

    if incident_priority is not None:
        priority_int = int(incident_priority)
        query = query.filter(models.Incident.incident_priority == priority_int)

    if incident_search is not None:
        query = query.filter((models.Incident.incident_name.contains(incident_search)) |
                             (models.Incident.incident_description.contains(incident_search)))
    return query.offset(skip).limit(limit).all()


def create_incident(db: Session, incident: schemas.IncidentBase):
    db_incident = models.Incident(incident_name=incident.incident_name,
                                  incident_description=incident.incident_description,
                                  incident_status=int(incident.incident_status),
                                  incident_priority=int(incident.incident_priority),
                                  incident_created_at=datetime.datetime.now(),
                                  incident_updated_at=datetime.datetime.now(),
                                  reporter_id=incident.reporter_id,
                                  resolver_id=incident.resolver_id)
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident


def get_incident(db: Session, incident_id: int):
    return db.query(models.Incident).filter(models.Incident.incident_id == incident_id).first()


def update_incident(incident_updated: schemas.IncidentUpdate, incident_found, db_session):
    incident_id = incident_found.incident_id
    result = db_session.query(models.Incident).filter(models.Incident.incident_id == incident_id).update({
        "incident_name": incident_updated.incident_name,
        "incident_description": incident_updated.incident_description,
        "incident_status": int(incident_updated.incident_status),
        "incident_priority": int(incident_updated.incident_priority),
        "incident_updated_at": datetime.datetime.now(),
        "resolver_id": incident_updated.resolver_id
    })
    db_session.commit()
    return result


def incident_delete(incident_id: int, db: Session):
    res = db.query(models.Incident).filter(models.Incident.incident_id == incident_id).delete()
    db.commit()
    return res


def connected_events_list(incident_id, event_id, db: Session, skip=0, limit=20):
    query = db.query(models.EventIncident)
    if incident_id is not None:
        query = query.filter(models.EventIncident.incident_id == incident_id)

    if event_id is not None:
        query = query.filter(models.EventIncident.event_id == event_id)

    return query.offset(skip).limit(limit).all()


def connected_events_create(incident_id: int, event_id: int, db: Session):
    connection = models.EventIncident(incident_id=incident_id, event_id=event_id)
    db.add(connection)
    db.commit()
    db.refresh(connection)
    return connection


def connected_events_delete(incident_id: int, event_id: int, db: Session):
    res = db.query(models.EventIncident).filter(models.EventIncident.incident_id == incident_id,
                                                models.EventIncident.event_id == event_id).delete()
    db.commit()
    return res


def comments_list(incident_id: int, db: Session):
    return db.query(models.Comment).filter(models.Comment.incident_id == incident_id).all()


def comment_create(incident_id: int, author_id: int, comment_text: str, db: Session):
    comment = models.Comment(incident_id=incident_id, author_id=author_id, comment_text=comment_text,
                             comment_created_at=datetime.datetime.now(),
                             comment_updated_at=datetime.datetime.now())
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def get_comment(db: Session, comment_id: int):
    return db.query(models.Comment).filter(models.Comment.comment_id == comment_id).first()


def update_comment(comment_text: str, comment_found, db_session: Session):
    comment_id = comment_found.comment_id
    result = db_session.query(models.Comment).filter(models.Comment.comment_id == comment_id).update({
        "comment_text": comment_text,
        "comment_updated_at": datetime.datetime.now(),
    })
    db_session.commit()
    return result


def comment_delete(comment_id: int, db: Session):
    res = db.query(models.Comment).filter(models.Comment.comment_id == comment_id).delete()
    db.commit()
    return res