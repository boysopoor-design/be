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


class AIGeneration(Base):
    __tablename__ = "AI_GENERATIONS"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    event_id = Column(
        Integer,
        ForeignKey("EVENTS.id"),
        nullable=True
    )

    generation_type = Column(
        String(100),
        nullable=False
    )

    input_data = Column(Text)

    output_data = Column(Text)

    model = Column(
        String(100),
        default="gpt-4o"
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    event = relationship(
        "Event",
        back_populates="ai_generations"
    )