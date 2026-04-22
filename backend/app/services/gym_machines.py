from sqlalchemy.orm import Session
from app.db.models.gym_machines import Gym_Machine
from fastapi import HTTPException

# CREATE
def services_gym_machine_create(db: Session, g_id: int, m_id: int, qty: int = 1):

    exist = db.query(Gym_Machine).filter(
        Gym_Machine.g_id == g_id,
        Gym_Machine.m_id == m_id
    ).first()

    if exist:
        raise HTTPException(status_code=400)

    try:
        obj = Gym_Machine(
            g_id=g_id,
            m_id=m_id,
            qty=qty
        )

        db.add(obj)
        db.commit()
        db.refresh(obj)

        return obj

    except Exception:
        db.rollback()
        raise HTTPException(status_code=500)


# UPDATE
def services_gym_machine_update(db: Session, g_id: int, m_id: int, qty: int):

    obj = db.query(Gym_Machine).filter(
        Gym_Machine.g_id == g_id,
        Gym_Machine.m_id == m_id
    ).first()

    if not obj:
        raise HTTPException(status_code=404)

    try:
        obj.qty = qty

        db.commit()
        db.refresh(obj)

        return obj

    except Exception:
        db.rollback()
        raise HTTPException(status_code=500)

# DELETE
def services_gym_machine_delete(db: Session, g_id: int, m_id: int):

    obj = db.query(Gym_Machine).filter(
        Gym_Machine.g_id == g_id,
        Gym_Machine.m_id == m_id
    ).first()

    if not obj:
        raise HTTPException(status_code=404)

    try:
        db.delete(obj)
        db.commit()

        return True

    except Exception:
        db.rollback()
        raise HTTPException(status_code=500)


# LIST (옵션 - 운동기구 조회용)
def services_gym_machine_get(db: Session, g_id: int):

    machines = (
        db.query(Gym_Machine)
        .filter(Gym_Machine.g_id == g_id)
        .all()
    )

    if not machines:
        raise HTTPException(status_code=404)

    return machines