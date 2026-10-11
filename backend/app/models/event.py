from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Numeric,
    ForeignKey,
    Text
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Event(Base):
    __tablename__ = "EVENTS"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255), nullable=False)
    event_type = Column(String(100))
    description = Column(Text)
    image_url = Column(Text, nullable=True)
    location = Column(String(255))

    event_date = Column(DateTime)

    attendees = Column(
        Integer,
        default=0
    )

    budget = Column(
        Numeric(18, 2),
        default=0
    )

    status = Column(
        String(50),
        default="PLANNING"
    )

    created_by = Column(
        Integer,
        ForeignKey("USERS.id"),
        nullable=False
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    creator = relationship(
        "User",
        back_populates="created_events"
    )

    departments = relationship(
        "Department",
        back_populates="event",
        cascade="all, delete-orphan"
    )

    tasks = relationship(
    "Task",
    back_populates="event",
    cascade="all, delete-orphan"
    )

    timeline_items = relationship(
        "TimelineItem",
        back_populates="event",
        cascade="all, delete-orphan"
    )

    report = relationship(
        "EventReport",
        back_populates="event",
        uselist=False,
        cascade="all, delete-orphan"
    )

    ai_generations = relationship(
        "AIGeneration",
        back_populates="event"
    )