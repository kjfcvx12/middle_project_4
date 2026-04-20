from sqlalchemy.orm import Session
from app.db.models.gym_staffs import Gym_Staff

def create(db: Session, obj: Gym_Staff):
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def delete(db: Session, obj: Gym_Staff):
    db.delete(obj)
    db.commit()