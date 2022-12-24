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
from src.endpoints.dependencies import BasicCommons

users_tag = "Users"
app = APIRouter()
base_url = dependencies.base_url


@app.get(base_url + "users", tags=[users_tag])
async def users_list(skip: NonNegativeInt = 0, limit: PositiveInt = 20,
                     commons: BasicCommons = Depends(BasicCommons), user_search: Union[str, None] = None):
    db_users = users.get_users(commons.db, skip=skip, limit=limit, user_search=user_search)
    return db_users


@app.post(base_url + "users", tags=[users_tag])
async def user_create(user: schemas.UserCreate, commons: BasicCommons = Depends(BasicCommons)):
    db = commons.db
    if user.user_role is None:
        raise HTTPException(status_code=422, detail="Role cannot be empty.")
    db_user = users.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return users.create_user(db=db, user=user)


@app.get(base_url + "users/{user_id}", tags=[users_tag])
async def user_view(user_id: NonNegativeInt, commons: BasicCommons = Depends(BasicCommons)):
    db = commons.db
    db_user = users.get_user_without_password(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put(base_url + "users", tags=[users_tag])
async def user_update(user_updated: schemas.User, commons: BasicCommons = Depends(BasicCommons)):
    db = commons.db
    user_found = db.query(models.User).filter(models.User.user_id == user_updated.user_id).first()
    if user_found is None:
        raise HTTPException(status_code=404, detail="User not found")
    users.update_user(user_updated=user_updated, user_found=user_found, db_session=db)
    return user_updated


@app.put(base_url + "users/{user_id}/passwd", tags=[users_tag])
async def user_update_passwd(user_id: NonNegativeInt, hashed_password: str, commons: BasicCommons = Depends(BasicCommons)):
    db = commons.db
    user_found = db.query(models.User).filter(models.User.user_id == user_id).first()
    if user_found is None:
        raise HTTPException(status_code=404, detail="User not found")
    requester = commons.current_user
    if requester.user_role is not int(UserRole.superuser):
        raise HTTPException(status_code=401, detail="User not admin")
    db_user = users.user_update_passwd(user_id=user_id, hashed_password=hashed_password, db_session=db)
    return db_user


@app.delete(base_url + "users/{user_id}", tags=[users_tag])
async def user_delete(user_id: NonNegativeInt, commons: BasicCommons = Depends(BasicCommons)):
    return users.user_delete(user_id, commons.db)


@app.get(base_url + "user-roles", tags=[users_tag])
async def user_roles(_: BasicCommons = Depends(BasicCommons)):
    return enum_to_json(UserRole)

