from datetime import timedelta

from fastapi import status
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.schemas import schemas
from src.endpoints import dependencies

users_tag = "Users"
app = APIRouter()
base_url = dependencies.base_url
get_db = dependencies.get_db


def get_token(user):
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


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(dependencies.get_db)):
    user = dependencies.authenticate_user(db, form_data.username, form_data.password)
    return get_token(user)


@app.post("/login", response_model=schemas.Token)
async def login_simple(login: schemas.Login,
                       db: Session = Depends(dependencies.get_db)):
    user = dependencies.authenticate_user(db, login.username, login.password)
    return get_token(user)
