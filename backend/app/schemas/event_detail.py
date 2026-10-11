from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class DepartmentDetail(BaseModel):
    id: int
    event_id: int
    name: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


class TaskDetail(BaseModel):
    id: int
    event_id: int
    department_id: int | None = None
    title: str
    description: str | None = None
    priority: str | None = None
    status: str | None = None
    progress: int | None = None
    start_date: datetime | None = None
    due_date: datetime | None = None
    assigned_to: int | None = None

    model_config = ConfigDict(from_attributes=True)


class TimelineItemDetail(BaseModel):
    id: int
    event_id: int
    title: str
    start_time: datetime
    end_time: datetime

    model_config = ConfigDict(from_attributes=True)


class EventDetailResponse(BaseModel):
    id: int
    name: str
    event_type: str | None = None
    description: str | None = None
    image_url: str | None = None
    location: str | None = None
    event_date: datetime | None = None
    attendees: int | None = None
    budget: Decimal | None = None
    status: str | None = None
    created_by: int
    created_at: datetime | None = None

    departments: list[DepartmentDetail]
    tasks: list[TaskDetail]
    timeline_items: list[TimelineItemDetail]