from typing import Union

from pydantic import BaseModel

from src.middle.UserRole import UserRole


class IncidentBase(BaseModel):
    title: str
    description: Union[str, None] = None


class Incident(IncidentBase):
    id: int

    class Config:
        orm_mode = True

"""
class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
"""


class UserBase(BaseModel):
    email: str
    user_role: UserRole


class UserCreate(UserBase):
    hashed_password: str


class User(UserBase):
    user_id: int
    is_active: bool

    class Config:
        orm_mode = True
