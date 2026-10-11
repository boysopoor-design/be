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


class Task(Base):
    __tablename__ = "TASKS"

    id = Column(Integer, primary_key=True, index=True)

    event_id = Column(Integer, ForeignKey("EVENTS.id"))

    department_id = Column(
        Integer,
        ForeignKey("DEPARTMENTS.id"),
        nullable=True
    )

    title = Column(
        String(255),
        nullable=False
    )

    description = Column(Text)

    priority = Column(
        String(20),
        default="MEDIUM"
    )

    status = Column(
        String(50),
        default="TODO"
    )

    progress = Column(
        Integer,
        default=0
    )

    start_date = Column(DateTime)
    due_date = Column(DateTime)

    assigned_to = Column(
        Integer,
        ForeignKey("USERS.id"),
        nullable=True
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    event = relationship(
        "Event",
        back_populates="tasks"
    )

    department = relationship(
        "Department",
        back_populates="tasks"
    )

    assignee = relationship(
        "User",
        back_populates="assigned_tasks"
    )