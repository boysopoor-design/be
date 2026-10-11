from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class EventReport(Base):
    __tablename__ = "EVENT_REPORTS"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    event_id = Column(
        Integer,
        ForeignKey("EVENTS.id"),
        nullable=False,
        unique=True
    )

    summary = Column(Text)
    achievements = Column(Text)
    problems = Column(Text)
    recommendations = Column(Text)

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    event = relationship(
        "Event",
        back_populates="report"
    )