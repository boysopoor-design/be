from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TimelineItemBase(BaseModel):
    title: str
    start_time: datetime
    end_time: datetime


class TimelineItemCreate(TimelineItemBase):
    event_id: int


class TimelineItemUpdate(BaseModel):
    title: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None


class TimelineItemResponse(TimelineItemBase):
    id: int
    event_id: int

    model_config = ConfigDict(from_attributes=True)