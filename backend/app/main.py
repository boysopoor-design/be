import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.auth import router as auth_router
from app.routers.events import router as events_router
from app.routers.departments import router as departments_router
from app.routers.tasks import router as tasks_router
from app.routers.timelines import router as timeline_router
from app.routers.reports import router as report_router
from app.routers.event_plan_ai import router as event_plan_ai_router

app = FastAPI(
    title="Mainstream Event Operating System",
    description="AI-powered Event Management Platform",
    version="1.0.0"
)

# Configure FRONTEND_ORIGINS in Railway as a comma-separated list if the
# frontend domain changes. Keep localhost origins for local development.
_default_origins = [
    "https://mainstream-7po.pages.dev",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
_frontend_origins = os.getenv("FRONTEND_ORIGINS", ",".join(_default_origins))
_allowed_origins = [origin.strip().rstrip("/") for origin in _frontend_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# =========================================================
# ROUTERS
# =========================================================

app.include_router(auth_router)

app.include_router(events_router)

app.include_router(departments_router)

app.include_router(tasks_router)

app.include_router(timeline_router)

app.include_router(report_router)
app.include_router(event_plan_ai_router)



# MVP schema bootstrap for fresh SQLite or PostgreSQL/Neon databases.
# create_all creates missing tables but does not alter existing tables, so the
# EVENTS.image_url compatibility migration is handled explicitly below.
@app.on_event("startup")
def bootstrap_database_schema():
    from sqlalchemy import inspect, text
    from app.core.database import engine, Base
    import app.models  # noqa: F401 - register every ORM model before create_all

    Base.metadata.create_all(bind=engine)
    inspector = inspect(engine)
    if "EVENTS" in inspector.get_table_names():
        columns = {column["name"] for column in inspector.get_columns("EVENTS")}
        if "image_url" not in columns:
            with engine.begin() as connection:
                connection.execute(text('ALTER TABLE "EVENTS" ADD COLUMN image_url TEXT'))


# =========================================================
# ROOT
# =========================================================

# Serve the Frontend login page at the root URL.


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }

