from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Department(Base):
    __tablename__ = "DEPARTMENTS"

    id = Column(Integer, primary_key=True, index=True)

    event_id = Column(
        Integer,
        ForeignKey("EVENTS.id"),
        nullable=False
    )

    name = Column(
        String(255),
        nullable=False
    )

    description = Column(Text)

    event = relationship(
        "Event",
        back_populates="departments"
    )

    tasks = relationship(
        "Task",
        back_populates="department"
    )