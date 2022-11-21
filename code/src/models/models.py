from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import DateTime
# from database.database import Base // this line is equal to the two below
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from src.middle import IncidentStatus
from src.middle.UserRole import UserRole

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    user_role = Column(Integer, nullable=False)


class Incident(Base):
    __tablename__ = "incidents"

    incident_id = Column(Integer, primary_key=True, index=True)
    incident_name = Column(String, nullable=False)
    incident_description = Column(String)
    incident_status = Column(Integer, nullable=False)
    incident_priority = Column(Integer, nullable=False)
    incident_created_at = Column(DateTime(timezone=True), nullable=False)
    incident_updated_at = Column(DateTime(timezone=True), nullable=False)
    reporter_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    resolver_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    @hybrid_property
    def is_opened(self):
        return IncidentStatus.is_opened(self.incident_status)


class EventIncident(Base):
    __tablename__ = "event_incidents"

    event_id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, primary_key=True, index=True)


class Comment(Base):
    __tablename__ = "comments"

    comment_id = Column(Integer, primary_key=True, index=True)
    comment_text = Column(String)
    comment_created_at = Column(DateTime(timezone=True), nullable=False)
    comment_updated_at = Column(DateTime(timezone=True), nullable=False)
    incident_id = Column(Integer, ForeignKey("incidents.incident_id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)


class Attachment(Base):
    __tablename__ = "attachments"

    attachment_id = Column(Integer, primary_key=True, index=True)
    attachment_path = Column(String, nullable=False)
    comment_id = Column(Integer, ForeignKey("comments.comment_id"), nullable=False)

