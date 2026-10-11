from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.timeline import TimelineItem
from app.models.event import Event
from app.models.user import User

from app.schemas.timeline import (
    TimelineItemCreate,
    TimelineItemUpdate,
    TimelineItemResponse
)


router = APIRouter(
    prefix="/api/timeline",
    tags=["Timeline"]
)


# =========================================================
# CREATE TIMELINE ITEM
# =========================================================

@router.post(
    "/",
    response_model=TimelineItemResponse
)
def create_timeline_item(
    timeline: TimelineItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # -----------------------------------------------------
    # Check Event belongs to current user
    # -----------------------------------------------------

    event = (
        db.query(Event)
        .filter(
            Event.id == timeline.event_id,
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
    # Create Timeline Item
    # -----------------------------------------------------

    new_item = TimelineItem(
        event_id=timeline.event_id,
        title=timeline.title,
        start_time=timeline.start_time,
        end_time=timeline.end_time
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item


# =========================================================
# GET ALL TIMELINE ITEMS
# =========================================================

@router.get(
    "/",
    response_model=list[TimelineItemResponse]
)
def get_timeline_items(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # -----------------------------------------------------
    # Only return timeline items belonging to
    # events owned by current user
    # -----------------------------------------------------

    timeline_items = (
        db.query(TimelineItem)
        .join(
            Event,
            TimelineItem.event_id == Event.id
        )
        .filter(
            Event.created_by == current_user.id
        )
        .all()
    )

    return timeline_items


# =========================================================
# GET TIMELINE ITEM BY ID
# =========================================================

@router.get(
    "/{timeline_id}",
    response_model=TimelineItemResponse
)
def get_timeline_item(
    timeline_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # -----------------------------------------------------
    # Timeline item must belong to an Event
    # owned by current user
    # -----------------------------------------------------

    item = (
        db.query(TimelineItem)
        .join(
            Event,
            TimelineItem.event_id == Event.id
        )
        .filter(
            TimelineItem.id == timeline_id,
            Event.created_by == current_user.id
        )
        .first()
    )

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Timeline item not found"
        )

    return item


# =========================================================
# UPDATE TIMELINE ITEM
# =========================================================

@router.put(
    "/{timeline_id}",
    response_model=TimelineItemResponse
)
def update_timeline_item(
    timeline_id: int,
    data: TimelineItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # -----------------------------------------------------
    # Timeline item must belong to an Event
    # owned by current user
    # -----------------------------------------------------

    item = (
        db.query(TimelineItem)
        .join(
            Event,
            TimelineItem.event_id == Event.id
        )
        .filter(
            TimelineItem.id == timeline_id,
            Event.created_by == current_user.id
        )
        .first()
    )

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Timeline item not found"
        )


    # -----------------------------------------------------
    # Update timeline item
    # -----------------------------------------------------

    update_data = data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)

    return item


# =========================================================
# DELETE TIMELINE ITEM
# =========================================================

@router.delete(
    "/{timeline_id}"
)
def delete_timeline_item(
    timeline_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # -----------------------------------------------------
    # Timeline item must belong to an Event
    # owned by current user
    # -----------------------------------------------------

    item = (
        db.query(TimelineItem)
        .join(
            Event,
            TimelineItem.event_id == Event.id
        )
        .filter(
            TimelineItem.id == timeline_id,
            Event.created_by == current_user.id
        )
        .first()
    )

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Timeline item not found"
        )


    # -----------------------------------------------------
    # Delete
    # -----------------------------------------------------

    db.delete(item)
    db.commit()

    return {
        "message": "Timeline item deleted successfully"
    }