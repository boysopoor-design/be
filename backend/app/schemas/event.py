from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional


class EventBase(BaseModel):
    name: str
    event_type: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    location: Optional[str] = None
    event_date: Optional[datetime] = None
    attendees: int = 0
    budget: Decimal = Decimal("0.00")
    status: str = "PLANNING"


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    name: Optional[str] = None
    event_type: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    location: Optional[str] = None
    event_date: Optional[datetime] = None
    attendees: Optional[int] = None
    budget: Optional[Decimal] = None
    status: Optional[str] = None


class EventResponse(EventBase):
    id: int
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True