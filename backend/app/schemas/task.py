from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "MEDIUM"
    status: str = "TODO"
    progress: int = 0
    start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    assigned_to: Optional[int] = None


class TaskCreate(TaskBase):
    event_id: int
    department_id: Optional[int] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    progress: Optional[int] = None
    start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    assigned_to: Optional[int] = None
    department_id: Optional[int] = None


class TaskResponse(TaskBase):
    id: int
    event_id: int
    department_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True