
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
    version="1.0.0",
)

# CORS: cho phép FE Cloudflare gọi BE Railway
origins = [
    origin.strip().rstrip("/")
    for origin in os.getenv(
        "FRONTEND_ORIGINS",
        "https://mainstream-7po.pages.dev",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routers
app.include_router(auth_router)
app.include_router(events_router)
app.include_router(departments_router)
app.include_router(tasks_router)
app.include_router(timeline_router)
app.include_router(report_router)
app.include_router(event_plan_ai_router)

@app.get("/")
def root():
    return {
        "message": "Mainstream Event Operating System",
        "status": "running",
    }
