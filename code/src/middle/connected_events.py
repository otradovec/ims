from sqlalchemy.orm import Session
from src.models import models


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
