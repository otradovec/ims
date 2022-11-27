import datetime

from sqlalchemy.orm import Session

from src.models import models
from src.schemas import schemas


def incident_list(incident_status, reporter_id, resolver_id, is_opened, incident_priority, incident_search,
                  skip, limit, db):
    query = db.query(models.Incident)
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


def update_incident_updated_at(incident_id, db):
    result = db.query(models.Incident).filter(models.Incident.incident_id == incident_id).update({
        "incident_updated_at": datetime.datetime.now(),
    })
    return result


def incident_delete(incident_id: int, db: Session):
    res = db.query(models.Incident).filter(models.Incident.incident_id == incident_id).delete()
    db.commit()
    return res
