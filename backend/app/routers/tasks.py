from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.models.task import Task
from app.models.event import Event
from app.models.department import Department
from app.models.user import User

from app.schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskResponse
)


router = APIRouter(
    prefix="/api/tasks",
    tags=["Tasks"]
)


# =========================================================
# CREATE TASK
# =========================================================

@router.post(
    "/",
    response_model=TaskResponse
)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # -----------------------------------------------------
    # Check Event belongs to current user
    # -----------------------------------------------------

    event = (
        db.query(Event)
        .filter(
            Event.id == task_data.event_id,
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
    # Check Department if provided
    # -----------------------------------------------------

    if task_data.department_id is not None:

        department = (
            db.query(Department)
            .filter(
                Department.id == task_data.department_id,
                Department.event_id == task_data.event_id
            )
            .first()
        )

        if not department:
            raise HTTPException(
                status_code=404,
                detail="Department not found or does not belong to this event"
            )


    # -----------------------------------------------------
    # Check assigned user if provided
    # -----------------------------------------------------

    if task_data.assigned_to is not None:

        assigned_user = (
            db.query(User)
            .filter(
                User.id == task_data.assigned_to
            )
            .first()
        )

        if not assigned_user:
            raise HTTPException(
                status_code=404,
                detail="Assigned user not found"
            )


    # -----------------------------------------------------
    # Create Task
    # -----------------------------------------------------

    task = Task(
        event_id=task_data.event_id,
        department_id=task_data.department_id,
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        status=task_data.status,
        progress=task_data.progress,
        start_date=task_data.start_date,
        due_date=task_data.due_date,
        assigned_to=task_data.assigned_to
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


# =========================================================
# GET ALL TASKS OF AN EVENT
# =========================================================

@router.get(
    "/event/{event_id}",
    response_model=list[TaskResponse]
)
def get_event_tasks(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # -----------------------------------------------------
    # Check Event belongs to current user
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
    # Get Tasks
    # -----------------------------------------------------

    tasks = (
        db.query(Task)
        .filter(
            Task.event_id == event_id
        )
        .all()
    )

    return tasks


# =========================================================
# GET TASK BY ID
# =========================================================

@router.get(
    "/{task_id}",
    response_model=TaskResponse
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # -----------------------------------------------------
    # Task must belong to an Event owned by current user
    # -----------------------------------------------------

    task = (
        db.query(Task)
        .join(Event, Task.event_id == Event.id)
        .filter(
            Task.id == task_id,
            Event.created_by == current_user.id
        )
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


# =========================================================
# UPDATE TASK
# =========================================================

@router.put(
    "/{task_id}",
    response_model=TaskResponse
)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # -----------------------------------------------------
    # Task must belong to an Event owned by current user
    # -----------------------------------------------------

    task = (
        db.query(Task)
        .join(Event, Task.event_id == Event.id)
        .filter(
            Task.id == task_id,
            Event.created_by == current_user.id
        )
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )


    # -----------------------------------------------------
    # Get update data
    # -----------------------------------------------------

    update_data = task_data.model_dump(
        exclude_unset=True
    )


    # -----------------------------------------------------
    # If department is being changed,
    # make sure it belongs to the same event
    # -----------------------------------------------------

    if "department_id" in update_data:

        new_department_id = update_data["department_id"]

        if new_department_id is not None:

            department = (
                db.query(Department)
                .filter(
                    Department.id == new_department_id,
                    Department.event_id == task.event_id
                )
                .first()
            )

            if not department:
                raise HTTPException(
                    status_code=400,
                    detail="Department does not belong to this event"
                )


    # -----------------------------------------------------
    # If assigned_to is being changed,
    # make sure the user exists
    # -----------------------------------------------------

    if "assigned_to" in update_data:

        new_assigned_to = update_data["assigned_to"]

        if new_assigned_to is not None:

            assigned_user = (
                db.query(User)
                .filter(
                    User.id == new_assigned_to
                )
                .first()
            )

            if not assigned_user:
                raise HTTPException(
                    status_code=404,
                    detail="Assigned user not found"
                )


    # -----------------------------------------------------
    # Apply changes
    # -----------------------------------------------------

    for key, value in update_data.items():
        setattr(task, key, value)


    db.commit()
    db.refresh(task)

    return task


# =========================================================
# DELETE TASK
# =========================================================

@router.delete(
    "/{task_id}"
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # -----------------------------------------------------
    # Task must belong to an Event owned by current user
    # -----------------------------------------------------

    task = (
        db.query(Task)
        .join(Event, Task.event_id == Event.id)
        .filter(
            Task.id == task_id,
            Event.created_by == current_user.id
        )
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )


    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted successfully"
    }
