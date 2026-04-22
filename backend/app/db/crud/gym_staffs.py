from sqlalchemy.orm import Session
from app.db.models.gym_staffs import Gym_Staff

# CREATE
def crud_gym_staffs_create(db: Session, obj: Gym_Staff):
    db.add(obj)
    db.flush()
    return obj

# DELETE
def crud_gym_staffs_delete(db: Session, obj: Gym_Staff):
    db.delete(obj)
    db.flush()

# LIST
def crud_gym_staffs_get(db: Session, g_id: int):
    return db.query(Gym_Staff).filter(
        Gym_Staff.g_id == g_id
    ).all()