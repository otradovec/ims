from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pydantic.types import NonNegativeInt
from sqlalchemy.orm import Session

from src.analysis_assistant.analysis_assistant import Assistant
from src.middle import incidents, users, UserRole
from src.models import models
from src.schemas import schemas
from src.database.database import engine
from src.endpoints import dependencies, login_endpoints, attachment_endpoints
from src.endpoints import incident_endpoints, connected_events_endpoints, comments_endpoints, users_endpoints

models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="IMS REST API documentation")

origins = {
    "http://localhost:3000",
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(incident_endpoints.app)
app.include_router(connected_events_endpoints.app)
app.include_router(comments_endpoints.app)
app.include_router(attachment_endpoints.app)
app.include_router(users_endpoints.app)
app.include_router(login_endpoints.app)


assistant_tag = "Analysis assistant"
assistant = Assistant()
base_url = dependencies.base_url


@app.get(base_url + "assistant/{incident_id}", tags=[assistant_tag])
async def advice_get(incident_id: NonNegativeInt, db: Session = Depends(dependencies.get_db),
                     current_user: schemas.User = Depends(dependencies.get_current_active_user)):
    db_incident = incidents.get_incident(db=db, incident_id=incident_id)
    if db_incident is None:
        raise HTTPException(status_code=422, detail="Incident not found")
    return assistant.advice_get(incident_id, db)


