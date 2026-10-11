from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class TimelineItem(Base):
    __tablename__ = "TIMELINE_ITEMS"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    event_id = Column(
        Integer,
        ForeignKey("EVENTS.id"),
        nullable=False
    )

    title = Column(
        String(255),
        nullable=False
    )

    start_time = Column(
        DateTime,
        nullable=False
    )

    end_time = Column(
        DateTime,
        nullable=False
    )

    event = relationship(
        "Event",
        back_populates="timeline_items"
    )