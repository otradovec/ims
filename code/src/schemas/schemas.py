import datetime
from typing import Union, Optional

from pydantic import BaseModel

from src.middle.IncidentPriority import IncidentPriority
from src.middle.UserRole import UserRole
from src.middle.IncidentStatus import IncidentStatus


class IncidentBase(BaseModel):
    incident_name: str
    incident_description: Union[str, None] = None
    incident_status = IncidentStatus
    incident_priority = IncidentPriority
    reporter_id = int
    resolver_id = int

    class Config:
        arbitrary_types_allowed = True


class IncidentFull(IncidentBase):
    incident_id: int
    incident_created_at = datetime
    incident_updated_at = datetime

    class Config:
        orm_mode = True


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
