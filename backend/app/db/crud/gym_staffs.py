from sqlalchemy.orm import Session
from app.db.models.gym_staffs import Gym_Staff

# CREATE
def create(db: Session, obj: Gym_Staff):
    db.add(obj)
    db.flush()
    return obj

# DELETE
def delete(db: Session, obj: Gym_Staff):
    db.delete(obj)
    db.flush()