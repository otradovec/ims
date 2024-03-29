import json
import os
import re

from sqlalchemy.orm import Session

from src.models import models
from src.schemas import schemas
from src.middle.UserRole import UserRole


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()


def get_user_without_password(db: Session, user_id: int):
    return db.query(models.User.user_id,
                    models.User.email,
                    models.User.is_active,
                    models.User.user_role).filter(models.User.user_id == user_id).first()


def get_user_by_email(db: Session, email: str) -> models.User:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users_without_password(db: Session, skip: int = 0, limit: int = 100, user_search: str = None):
    if user_search is not None:
        #  Filter like must be applied directly to new query, otherwise produces RecursiveError
        query = db.query(models.User.user_id, models.User.email, models.User.is_active, models.User.user_role) \
            .filter(models.User.email.like(user_search + '%'))
    else:
        query = db.query(models.User.user_id, models.User.email, models.User.is_active, models.User.user_role)
    query = query.offset(skip).limit(limit)
    return query.all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, hashed_password=user.hashed_password, user_role=int(user.user_role))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(user_updated: schemas.User, user_found: schemas.User, db_session: Session):
    user_id = user_found.user_id
    result = db_session.query(models.User).filter(models.User.user_id == user_id).update({
        "user_id": user_found.user_id,
        "email": user_updated.email,
        "user_role": int(user_updated.user_role),
        "is_active": user_updated.is_active
    })
    db_session.commit()
    return result


def user_update_passwd(user_id, hashed_password, db_session):
    result = db_session.query(models.User).filter(models.User.user_id == user_id).update({
        "hashed_password": hashed_password,
    })
    db_session.commit()
    return result


def user_delete(user_id, db):
    res = db.query(models.User).filter(models.User.user_id == user_id).delete()
    db.commit()
    return res


def get_secrets():
    fpath = os.path.join(os.getcwd(), "src", "middle", ".secrets")
    with open(fpath, "r") as f:
        lines = f.readlines()
    lines_str = "\n".join(lines)
    json_secrets = json.loads(lines_str)
    return json_secrets["secrets"]


def create_superuser(db):
    secret = get_secrets()[0]
    secret_hash = secret["hash"]
    secret_email = secret["email"]
    db_user = models.User(email=secret_email, hashed_password=secret_hash, user_role=int(UserRole.superuser))
    if get_user_by_email(db, secret_email) is None:
        create_user(db, user=db_user)


def valid_email(email) -> bool:
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    return bool(re.fullmatch(regex, email))
