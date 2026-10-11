from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class User(Base):
    __tablename__ = "USERS"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    full_name = Column(
        String(255),
        nullable=False
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = Column(
        String(255),
        nullable=False
    )

    role = Column(
        String(50),
        default="USER"
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    created_events = relationship(
        "Event",
        back_populates="creator"
    )

    assigned_tasks = relationship(
        "Task",
        back_populates="assignee"
    )