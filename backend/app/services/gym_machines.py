from sqlalchemy.orm import Session
from app.db.models.gym_machines import Gym_Machine

# CREATE
def createGymMachineService(db: Session, g_id: int, m_id: int, qty: int):
    exist = db.query(Gym_Machine).filter(
        Gym_Machine.g_id == g_id,
        Gym_Machine.m_id == m_id
    ).first()

    if exist:
        return None

    obj = Gym_Machine(
        g_id=g_id,
        m_id=m_id,
        qty=qty
    )

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj

# UPDATE
def updateGymMachineService(db: Session, g_id: int, m_id: int, qty: int):
    obj = db.query(Gym_Machine).filter(
        Gym_Machine.g_id == g_id,
        Gym_Machine.m_id == m_id
    ).first()

    if not obj:
        return None

    obj.qty = qty

    db.commit()
    db.refresh(obj)

    return obj

# DELETE
def deleteGymMachineService(db: Session, g_id: int, m_id: int):
    obj = db.query(Gym_Machine).filter(
        Gym_Machine.g_id == g_id,
        Gym_Machine.m_id == m_id
    ).first()

    if not obj:
        return None

    db.delete(obj)
    db.commit()

    return True