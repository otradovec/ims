from datetime import datetime
from typing import Union, Optional

from pydantic import BaseModel
from pydantic import Field
from pydantic.types import NonNegativeInt


from src.middle.IncidentPriority import IncidentPriority
from src.middle.UserRole import UserRole
from src.middle.IncidentStatus import IncidentStatus

example_incident_description = "Reports devices that communicate with blacklisted IP addresses. This may indicate " \
                               "that a device is compromised or takes part in malicious activities depending on the " \
                               "category of the blacklisted IP address. Known botnet C&C center, attempts: 4," \
                               " uploaded: 22.84 MiB, downloaded: 0 B, frequently used ports: 2048."


class IncidentBase(BaseModel):
    incident_name: str = Field(example="Detected communication with blacklisted hosts")
    incident_description: Union[str, None] = Field(default=None, example=example_incident_description)
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
    email: str = Field(example="henry.ford@redhat.com")
    user_role: UserRole


class UserCreate(UserBase):
    hashed_password: str


class User(UserBase):
    user_id: NonNegativeInt
    is_active: bool

    class Config:
        orm_mode = True


class CommentBase(BaseModel):
    comment_text: Union[str, None] = Field(default=None, example="Used protocol is ICMP")


class CommentCreate(CommentBase):
    author_id: NonNegativeInt
    incident_id: NonNegativeInt


class CommentDetail(CommentCreate):
    comment_id: NonNegativeInt
    comment_created_at: datetime
    comment_updated_at: datetime


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Union[int, None] = None
