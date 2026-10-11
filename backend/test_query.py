from app.core.database import SessionLocal
from app.models import User, Event


db = SessionLocal()

try:
    users = db.query(User).all()
    events = db.query(Event).all()

    print("Users:", len(users))
    print("Events:", len(events))

finally:
    db.close()