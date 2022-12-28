from typing import Union

from fastapi import APIRouter
from fastapi import Depends, HTTPException
from pydantic.types import NonNegativeInt, PositiveInt

from src.middle import connected_events, incidents
from src.schemas import schemas
from src.endpoints import dependencies
from src.endpoints.dependencies import BasicCommons
from src.flowmon_api import is_real_event

app = APIRouter()
base_url = dependencies.base_url
connected_events_tag = "Connected Events"


@app.get(base_url + "connected-events", tags=[connected_events_tag])
async def connected_events_list(incident_id: Union[NonNegativeInt, None] = None,
                                event_id: Union[NonNegativeInt, None] = None,
                                skip: NonNegativeInt = 0, limit: PositiveInt = 20,
                                commons: BasicCommons = Depends(BasicCommons)):
    return connected_events.connected_events_list(incident_id=incident_id, event_id=event_id, skip=skip, limit=limit,
                                                  db=commons.db)


@app.post(base_url + "connected-events", tags=[connected_events_tag])
async def connected_events_create(connected_event: schemas.ConnectedEvent = Depends(),
                                  commons: BasicCommons = Depends(BasicCommons)):
    existing_connections_list = connected_events.connected_events_list(connected_event.incident_id,
                                                                       connected_event.event_id, commons.db)
    if not is_real_event(connected_event.event_id):
        raise HTTPException(status_code=422, detail="Event with event_id not existing")

    if len(existing_connections_list) > 0:
        raise HTTPException(status_code=400, detail="Connection already present")

    incident = incidents.get_incident(commons.db, connected_event.incident_id)
    if incident is None:
        raise HTTPException(status_code=400, detail="No incident with incident_id")

    return connected_events.connected_events_create(connected_event, commons.db)


@app.delete(base_url + "connected-events", tags=[connected_events_tag])
async def connected_events_delete(connected_event: schemas.ConnectedEvent = Depends(),
                                  commons: BasicCommons = Depends(BasicCommons)):
    return connected_events.connected_events_delete(connected_event, commons.db)
