from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ReportBase(BaseModel):
    summary: str | None = None
    achievements: str | None = None
    problems: str | None = None
    recommendations: str | None = None


class ReportCreate(ReportBase):
    event_id: int


class ReportUpdate(BaseModel):
    summary: str | None = None
    achievements: str | None = None
    problems: str | None = None
    recommendations: str | None = None


class ReportResponse(ReportBase):
    id: int
    event_id: int
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)