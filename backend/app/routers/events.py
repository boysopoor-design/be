from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User
from app.models.event import Event
from app.models import Department, Task, TimelineItem

from app.schemas.event import (
    EventCreate,
    EventResponse,
    EventUpdate
)

from app.schemas.event_detail import EventDetailResponse


router = APIRouter(
    prefix="/api/events",
    tags=["Events"]
)


# =========================================================
# CREATE EVENT
# =========================================================

@router.post(
    "/",
    response_model=EventResponse
)
def create_event(
    event_data: EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    event = Event(
        name=event_data.name,
        event_type=event_data.event_type,
        description=event_data.description,
        image_url=event_data.image_url,
        location=event_data.location,
        event_date=event_data.event_date,
        attendees=event_data.attendees,
        budget=event_data.budget,
        status=event_data.status,

        # User đang đăng nhập sẽ trở thành owner
        created_by=current_user.id
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return event


# =========================================================
# GET ALL EVENTS OF CURRENT USER
# =========================================================

@router.get(
    "/",
    response_model=list[EventResponse]
)
def get_events(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    events = (
        db.query(Event)
        .filter(
            Event.created_by == current_user.id
        )
        .all()
    )

    return events


# =========================================================
# GET EVENT DETAIL
# =========================================================

@router.get(
    "/{event_id}/detail",
    response_model=EventDetailResponse
)
def get_event_detail(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # -----------------------------------------------------
    # Get Event
    # Only allow owner to access it
    # -----------------------------------------------------

    event = (
        db.query(Event)
        .filter(
            Event.id == event_id,
            Event.created_by == current_user.id
        )
        .first()
    )

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )


    # -----------------------------------------------------
    # Get Departments
    # -----------------------------------------------------

    departments = (
        db.query(Department)
        .filter(
            Department.event_id == event_id
        )
        .all()
    )


    # -----------------------------------------------------
    # Get Tasks
    # -----------------------------------------------------

    tasks = (
        db.query(Task)
        .filter(
            Task.event_id == event_id
        )
        .all()
    )


    # -----------------------------------------------------
    # Get Timeline Items
    # -----------------------------------------------------

    timeline_items = (
        db.query(TimelineItem)
        .filter(
            TimelineItem.event_id == event_id
        )
        .all()
    )


    # -----------------------------------------------------
    # Return Event Detail
    # -----------------------------------------------------

    return {
        "id": event.id,
        "name": event.name,
        "event_type": event.event_type,
        "description": event.description,
        "image_url": event.image_url,
        "location": event.location,
        "event_date": event.event_date,
        "attendees": event.attendees,
        "budget": event.budget,
        "status": event.status,
        "created_by": event.created_by,
        "created_at": event.created_at,

        "departments": departments,
        "tasks": tasks,
        "timeline_items": timeline_items
    }


# =========================================================
# GET EVENT BY ID
# =========================================================

@router.get(
    "/{event_id}",
    response_model=EventResponse
)
def get_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    event = (
        db.query(Event)
        .filter(
            Event.id == event_id,
            Event.created_by == current_user.id
        )
        .first()
    )

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    return event


# =========================================================
# UPDATE EVENT
# =========================================================

@router.put(
    "/{event_id}",
    response_model=EventResponse
)
def update_event(
    event_id: int,
    event_data: EventUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    event = (
        db.query(Event)
        .filter(
            Event.id == event_id,
            Event.created_by == current_user.id
        )
        .first()
    )

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )


    update_data = event_data.model_dump(
        exclude_unset=True
    )


    for key, value in update_data.items():
        setattr(event, key, value)


    db.commit()
    db.refresh(event)

    return event


# =========================================================
# DELETE EVENT
# =========================================================

@router.delete(
    "/{event_id}"
)
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    event = (
        db.query(Event)
        .filter(
            Event.id == event_id,
            Event.created_by == current_user.id
        )
        .first()
    )

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )


    db.delete(event)
    db.commit()

    return {
        "message": "Event deleted successfully"
    }