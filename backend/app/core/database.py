from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./mainstream.db")

# Railway may provide PostgreSQL URLs as postgres://. SQLAlchemy's psycopg2
# driver expects postgresql://, so normalize the scheme before creating the engine.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = "postgresql://" + DATABASE_URL[len("postgres://"):]

# Keep local SQLite paths anchored to the backend directory, regardless of
# which working directory is used to start Uvicorn. PostgreSQL URLs pass through.
if DATABASE_URL.startswith("sqlite:///./"):
    from pathlib import Path
    _db_name = DATABASE_URL.removeprefix("sqlite:///./")
    _db_path = (Path(__file__).resolve().parents[2] / _db_name).resolve()
    DATABASE_URL = "sqlite:///" + _db_path.as_posix()

engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# SQLAlchemy models use func.now(), supported by SQLite and PostgreSQL.
