from sqlalchemy.orm import Session
from app.db.models.gym_machines import Gym_Machine

# CREATE
def crud_gym_machine_create(db: Session, obj: Gym_Machine):
    db.add(obj)
    db.flush()
    return obj

# READ
def crud_gym_machine_get(db: Session, g_id: int, m_id: int):
    return db.query(Gym_Machine).filter(
        Gym_Machine.g_id == g_id,
        Gym_Machine.m_id == m_id
    ).first()

# UPDATE
def crud_gym_machine_update(db: Session, obj: Gym_Machine, qty: int):
    obj.qty = qty
    db.flush()
    return obj

# DELETE
def crud_gym_machine_delete(db: Session, obj: Gym_Machine):
    db.delete(obj)
    db.flush()

# LIST
def crud_gym_machines_get_id(db: Session, g_id: int):
    return db.query(Gym_Machine).filter(
        Gym_Machine.g_id == g_id
    ).all()