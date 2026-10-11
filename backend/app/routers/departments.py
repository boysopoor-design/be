from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.department import Department
from app.models.event import Event
from app.models.user import User

from app.schemas.department import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse
)


router = APIRouter(
    prefix="/api/departments",
    tags=["Departments"]
)


# =========================================================
# CREATE DEPARTMENT
# =========================================================

@router.post(
    "/",
    response_model=DepartmentResponse
)
def create_department(
    department_data: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Check Event exists AND belongs to current user
    event = (
        db.query(Event)
        .filter(
            Event.id == department_data.event_id,
            Event.created_by == current_user.id
        )
        .first()
    )

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    department = Department(
        event_id=department_data.event_id,
        name=department_data.name,
        description=department_data.description
    )

    db.add(department)
    db.commit()
    db.refresh(department)

    return department


# =========================================================
# GET ALL DEPARTMENTS OF AN EVENT
# =========================================================

@router.get(
    "/event/{event_id}",
    response_model=list[DepartmentResponse]
)
def get_departments(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Check Event exists AND belongs to current user
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

    departments = (
        db.query(Department)
        .filter(
            Department.event_id == event_id
        )
        .all()
    )

    return departments


# =========================================================
# GET DEPARTMENT BY ID
# =========================================================

@router.get(
    "/{department_id}",
    response_model=DepartmentResponse
)
def get_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Join Department -> Event
    # to make sure the event belongs to current user
    department = (
        db.query(Department)
        .join(Event, Department.event_id == Event.id)
        .filter(
            Department.id == department_id,
            Event.created_by == current_user.id
        )
        .first()
    )

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    return department


# =========================================================
# UPDATE DEPARTMENT
# =========================================================

@router.put(
    "/{department_id}",
    response_model=DepartmentResponse
)
def update_department(
    department_id: int,
    department_data: DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Find department only if its event belongs to current user
    department = (
        db.query(Department)
        .join(Event, Department.event_id == Event.id)
        .filter(
            Department.id == department_id,
            Event.created_by == current_user.id
        )
        .first()
    )

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    update_data = department_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(department, key, value)

    db.commit()
    db.refresh(department)

    return department


# =========================================================
# DELETE DEPARTMENT
# =========================================================

@router.delete(
    "/{department_id}"
)
def delete_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Find department only if its event belongs to current user
    department = (
        db.query(Department)
        .join(Event, Department.event_id == Event.id)
        .filter(
            Department.id == department_id,
            Event.created_by == current_user.id
        )
        .first()
    )

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    db.delete(department)
    db.commit()

    return {
        "message": "Department deleted successfully"
    }
