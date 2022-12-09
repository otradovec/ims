from typing import Union

from fastapi import APIRouter
from fastapi import Depends, HTTPException
from pydantic.types import NonNegativeInt, PositiveInt
from sqlalchemy.orm import Session

from src.middle import connected_events, incidents
from src.schemas import schemas
from src.endpoints import dependencies


app = APIRouter()
base_url = dependencies.base_url
connected_events_tag = "Connected Events"
get_db = dependencies.get_db


@app.get(base_url + "connected-events", tags=[connected_events_tag])
async def connected_events_list(incident_id: Union[NonNegativeInt, None] = None,
                                event_id: Union[NonNegativeInt, None] = None,
                                skip: NonNegativeInt = 0, limit: PositiveInt = 20,
                                db: Session = Depends(get_db),
                                current_user: schemas.User = Depends(dependencies.get_current_active_user)):
    return connected_events.connected_events_list(incident_id=incident_id, event_id=event_id, skip=skip, limit=limit,
                                                  db=db)


@app.post(base_url + "connected-events", tags=[connected_events_tag])
async def connected_events_create(connected_event: schemas.ConnectedEvent = Depends(), db: Session = Depends(get_db),
                                  current_user: schemas.User = Depends(dependencies.get_current_active_user)):
    existing_connections_list = connected_events.connected_events_list(connected_event.incident_id,
                                                                       connected_event.event_id, db)
    if len(existing_connections_list) > 0:
        raise HTTPException(status_code=400, detail="Connection already present")

    incident = incidents.get_incident(db, connected_event.incident_id)
    if incident is None:
        raise HTTPException(status_code=400, detail="No incident with incident_id")

    return connected_events.connected_events_create(connected_event, db)


@app.delete(base_url + "connected-events", tags=[connected_events_tag])
async def connected_events_delete(connected_event: schemas.ConnectedEvent = Depends(), db: Session = Depends(get_db),
                                  current_user: schemas.User = Depends(dependencies.get_current_active_user)):
    return connected_events.connected_events_delete(connected_event, db)