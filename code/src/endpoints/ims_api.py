from fastapi import Depends, FastAPI, HTTPException
from pydantic.types import NonNegativeInt
from sqlalchemy.orm import Session

from src.analysis_assistant.analysis_assistant import Assistant
from src.middle import incidents
from src.models import models
from src.schemas import schemas
from src.database.database import engine
from src.endpoints import dependencies
from src.endpoints import incident_endpoints, connected_events_endpoints, comments_endpoints, users_endpoints

models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="IMS REST API documentation")
app.include_router(incident_endpoints.app)
app.include_router(connected_events_endpoints.app)
app.include_router(comments_endpoints.app)
app.include_router(users_endpoints.app)

assistant_tag = "Analysis assistant"
assistant = Assistant()
base_url = dependencies.base_url


@app.get(base_url + "assistant/{incident_id}", tags=[assistant_tag])
async def advice_get(incident_id: NonNegativeInt, db: Session = Depends(dependencies.get_db)):
    db_incident = incidents.get_incident(db=db, incident_id=incident_id)
    if db_incident is None:
        raise HTTPException(status_code=422, detail="Incident not found")
    return assistant.advice_get(incident_id, db)
