from sqlalchemy.orm import Session
from app.db.models.gym_machines import Gym_Machine


# CREATE
def createGymMachine(db: Session, obj: Gym_Machine):
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


# READ
def getGymMachine(db: Session, g_id: int, m_id: int):
    return db.query(Gym_Machine).filter(
        Gym_Machine.g_id == g_id,
        Gym_Machine.m_id == m_id
    ).first()


# UPDATE
def updateGymMachine(db: Session, obj: Gym_Machine, qty: int):
    obj.qty = qty
    db.commit()
    db.refresh(obj)
    return obj


# DELETE
def deleteGymMachine(db: Session, obj: Gym_Machine):
    db.delete(obj)
    db.commit()


# LIST
def getGymMachines(db: Session, g_id: int):
    return db.query(Gym_Machine).filter(
        Gym_Machine.g_id == g_id
    ).all()