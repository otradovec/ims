from sqlalchemy.orm import Session
from src.models import models
from src.schemas import schemas


def connected_events_list(incident_id, event_id, db: Session, skip=0, limit=20):
    query = db.query(models.EventIncident)
    if incident_id is not None:
        query = query.filter(models.EventIncident.incident_id == incident_id)

    if event_id is not None:
        query = query.filter(models.EventIncident.event_id == event_id)

    return query.offset(skip).limit(limit).all()


def connected_events_create(connected_event: schemas.ConnectedEvent, db: Session):
    connection = models.EventIncident(**connected_event.dict())
    db.add(connection)
    db.commit()
    db.refresh(connection)
    return connection


def connected_events_delete(connected_event: schemas.ConnectedEvent, db: Session):
    res = db.query(models.EventIncident).filter(models.EventIncident.incident_id == connected_event.incident_id,
                                                models.EventIncident.event_id == connected_event.event_id).delete()
    db.commit()
    return res
