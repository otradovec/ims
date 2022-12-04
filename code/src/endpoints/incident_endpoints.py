from fastapi import APIRouter
from fastapi import Depends, HTTPException
from pydantic.types import NonNegativeInt, PositiveInt
from sqlalchemy.orm import Session

from src.middle.enum_to_json import enum_to_json
from src.middle.IncidentPriority import IncidentPriority
from src.middle.IncidentStatus import IncidentStatus
from src.middle import incidents, users
from src.models import models
from src.schemas import schemas
from src.endpoints import dependencies


app = APIRouter()
incident_tag = "Incidents"
base_url = dependencies.base_url
get_db = dependencies.get_db


@app.get(base_url + "incidents", tags=[incident_tag])
async def incidents_list(search_params: schemas.IncidentSearch = Depends(), skip: NonNegativeInt = 0,
                         limit: PositiveInt = 20, db: Session = Depends(get_db)
                         ):
    return incidents.incident_list(**search_params.dict(), skip=skip, limit=limit, db=db)


@app.post(base_url + "incidents", tags=[incident_tag])
async def incident_create(incident: schemas.IncidentCreate, db: Session = Depends(get_db)):
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
async def incident_detail(incident_id: NonNegativeInt, db: Session = Depends(get_db)):
    db_incident = incidents.get_incident(db, incident_id=incident_id)
    if db_incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return db_incident


@app.delete(base_url + "incidents/{incident_id}", tags=[incident_tag])
async def incident_delete(incident_id: NonNegativeInt, db: Session = Depends(get_db)):
    return incidents.incident_delete(incident_id, db)


@app.get(base_url + "incident-states", tags=[incident_tag])
async def incident_states():
    return enum_to_json(IncidentStatus)


@app.get(base_url + "incident-priorities", tags=[incident_tag])
async def incident_priorities():
    return enum_to_json(IncidentPriority)
