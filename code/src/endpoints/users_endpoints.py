from typing import Union

from fastapi import Depends, HTTPException, APIRouter
from pydantic.types import NonNegativeInt, PositiveInt
from sqlalchemy.orm import Session

from src.middle.UserRole import UserRole
from src.middle.enum_to_json import enum_to_json
from src.middle import users
from src.models import models
from src.schemas import schemas
from src.endpoints import dependencies

users_tag = "Users"
app = APIRouter()
base_url = dependencies.base_url
get_db = dependencies.get_db


@app.get(base_url + "users", tags=[users_tag])
async def users_list(skip: NonNegativeInt = 0, limit: PositiveInt = 20,
                     db: Session = Depends(dependencies.get_db), user_search: Union[str, None] = None):
    db_users = users.get_users(db, skip=skip, limit=limit, user_search=user_search)
    return db_users


@app.post(base_url + "users", tags=[users_tag])
async def user_create(user: schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
    if user.user_role is None:
        raise HTTPException(status_code=422, detail="Role cannot be empty.")
    db_user = users.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return users.create_user(db=db, user=user)


@app.get(base_url + "users/{user_id}", tags=[users_tag])
async def user_view(user_id: NonNegativeInt, db: Session = Depends(dependencies.get_db)):
    db_user = users.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put(base_url + "users", tags=[users_tag])
async def user_update(user_updated: schemas.User, db: Session = Depends(dependencies.get_db)):
    user_found = db.query(models.User).filter(models.User.user_id == user_updated.user_id).first()
    if user_found is None:
        raise HTTPException(status_code=404, detail="User not found")
    users.update_user(user_updated=user_updated, user_found=user_found, db_session=db)
    return user_updated


@app.put(base_url + "users/{user_id}/passwd", tags=[users_tag])
async def user_update_passwd(user_id: NonNegativeInt, hashed_password: str, db: Session = Depends(dependencies.get_db)):
    user_found = db.query(models.User).filter(models.User.user_id == user_id).first()
    if user_found is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user = users.user_update_passwd(user_id=user_id, user_passwd=hashed_password, db_session=db)
    return db_user


@app.delete(base_url + "users/{user_id}", tags=[users_tag])
async def user_delete(user_id: NonNegativeInt, db: Session = Depends(dependencies.get_db)):
    return users.user_delete(user_id, db)


@app.get(base_url + "user-roles", tags=[users_tag])
async def user_roles():
    return enum_to_json(UserRole)

