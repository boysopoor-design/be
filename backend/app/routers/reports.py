from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.user import User
from app.models.event import Event
from app.models.report import EventReport

from app.schemas.report import (
    ReportCreate,
    ReportUpdate,
    ReportResponse
)


router = APIRouter(
    prefix="/api/reports",
    tags=["Reports"]
)


# ==========================================
# CREATE REPORT
# ==========================================

@router.post(
    "/",
    response_model=ReportResponse
)
def create_report(
    report: ReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # ------------------------------------------
    # Check Event belongs to current user
    # ------------------------------------------

    event = (
        db.query(Event)
        .filter(
            Event.id == report.event_id,
            Event.created_by == current_user.id
        )
        .first()
    )

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )


    # ------------------------------------------
    # Check existing report
    # ------------------------------------------

    existing_report = (
        db.query(EventReport)
        .filter(
            EventReport.event_id == report.event_id
        )
        .first()
    )

    if existing_report:
        raise HTTPException(
            status_code=400,
            detail="This event already has a report"
        )


    # ------------------------------------------
    # Create report
    # ------------------------------------------

    new_report = EventReport(
        event_id=report.event_id,
        summary=report.summary,
        achievements=report.achievements,
        problems=report.problems,
        recommendations=report.recommendations
    )

    db.add(new_report)
    db.commit()
    db.refresh(new_report)

    return new_report


# ==========================================
# GET REPORT BY ID
# ==========================================

@router.get(
    "/{report_id}",
    response_model=ReportResponse
)
def get_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # ------------------------------------------
    # Report must belong to user's Event
    # ------------------------------------------

    report = (
        db.query(EventReport)
        .join(
            Event,
            EventReport.event_id == Event.id
        )
        .filter(
            EventReport.id == report_id,
            Event.created_by == current_user.id
        )
        .first()
    )

    if not report:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    return report


# ==========================================
# GET REPORT BY EVENT
# ==========================================

@router.get(
    "/event/{event_id}",
    response_model=ReportResponse
)
def get_report_by_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # ------------------------------------------
    # Check Event belongs to current user
    # ------------------------------------------

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


    # ------------------------------------------
    # Get report
    # ------------------------------------------

    report = (
        db.query(EventReport)
        .filter(
            EventReport.event_id == event_id
        )
        .first()
    )

    if not report:
        raise HTTPException(
            status_code=404,
            detail="Report not found for this event"
        )

    return report


# ==========================================
# UPDATE REPORT
# ==========================================

@router.put(
    "/event/{event_id}",
    response_model=ReportResponse
)
def update_report(
    event_id: int,
    data: ReportUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # ------------------------------------------
    # Find report through owned Event
    # ------------------------------------------

    report = (
        db.query(EventReport)
        .join(
            Event,
            EventReport.event_id == Event.id
        )
        .filter(
            EventReport.event_id == event_id,
            Event.created_by == current_user.id
        )
        .first()
    )

    if not report:
        raise HTTPException(
            status_code=404,
            detail="Report not found for this event"
        )


    # ------------------------------------------
    # Update report
    # ------------------------------------------

    update_data = data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(report, key, value)

    db.commit()
    db.refresh(report)

    return report


# ==========================================
# DELETE REPORT
# ==========================================

@router.delete(
    "/event/{event_id}"
)
def delete_report(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # ------------------------------------------
    # Find report through owned Event
    # ------------------------------------------

    report = (
        db.query(EventReport)
        .join(
            Event,
            EventReport.event_id == Event.id
        )
        .filter(
            EventReport.event_id == event_id,
            Event.created_by == current_user.id
        )
        .first()
    )

    if not report:
        raise HTTPException(
            status_code=404,
            detail="Report not found for this event"
        )


    # ------------------------------------------
    # Delete report
    # ------------------------------------------

    db.delete(report)
    db.commit()

    return {
        "message": "Report deleted successfully"
    }
