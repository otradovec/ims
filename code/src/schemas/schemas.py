from datetime import datetime
from typing import Union, Optional

from pydantic import BaseModel
from pydantic.types import NonNegativeInt


from src.middle.IncidentPriority import IncidentPriority
from src.middle.UserRole import UserRole
from src.middle.IncidentStatus import IncidentStatus


class IncidentBase(BaseModel):
    incident_name: str
    incident_description: Union[str, None] = None
    incident_status: IncidentStatus = IncidentStatus.reported
    incident_priority: IncidentPriority = IncidentPriority.medium
    resolver_id: NonNegativeInt

    class Config:
        arbitrary_types_allowed = True


class IncidentCreate(IncidentBase):
    reporter_id: NonNegativeInt


class IncidentFull(IncidentCreate):
    incident_id: NonNegativeInt
    incident_created_at: datetime
    incident_updated_at: datetime

    class Config:
        orm_mode = True


class IncidentUpdate(IncidentBase):
    incident_id: NonNegativeInt


# Has to be BaseModel child because of optional attributes
class IncidentSearch(BaseModel):
    incident_status: IncidentStatus = None
    reporter_id: NonNegativeInt = None
    resolver_id: NonNegativeInt = None
    is_opened: Optional[bool] = None
    incident_priority: IncidentPriority = None
    incident_search: Optional[str] = None


class ConnectedEvent(BaseModel):
    incident_id: NonNegativeInt
    event_id: NonNegativeInt


class UserBase(BaseModel):
    email: str
    user_role: UserRole


class UserCreate(UserBase):
    hashed_password: str


class User(UserBase):
    user_id: NonNegativeInt
    is_active: bool

    class Config:
        orm_mode = True


class CommentBase(BaseModel):
    comment_text: Union[str, None] = None


class CommentCreate(CommentBase):
    author_id: NonNegativeInt
    incident_id: NonNegativeInt


class CommentDetail(CommentCreate):
    comment_id: NonNegativeInt
    comment_created_at: datetime
    comment_updated_at: datetime

