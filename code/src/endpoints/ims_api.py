from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from pydantic.types import NonNegativeInt
from sqlalchemy.orm import Session

from src.analysis_assistant.analysis_assistant import Assistant
from src.middle import incidents, users, UserRole
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
async def advice_get(incident_id: NonNegativeInt, db: Session = Depends(dependencies.get_db),
                     current_user: schemas.User = Depends(dependencies.get_current_active_user)):
    db_incident = incidents.get_incident(db=db, incident_id=incident_id)
    if db_incident is None:
        raise HTTPException(status_code=422, detail="Incident not found")
    return assistant.advice_get(incident_id, db)


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(dependencies.get_db)):
    user = dependencies.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=dependencies.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = dependencies.create_access_token(
        data={"userid": user.user_id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

