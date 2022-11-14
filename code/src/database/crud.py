from sqlalchemy.orm import Session, load_only

from src.models import models
from src.schemas import schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100, user_search: str = None):
    query = db.query(models.User).offset(skip).limit(limit).options(load_only(models.User.user_id, models.User.email, models.User.is_active, models.User.user_role))
    if user_search is None:
        return query.all()
    else:
        return query.filter(models.User.email.like('%' + user_search + '%')).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.hashed_password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password, user_role=user.user_role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

"""
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
"""