from sqlalchemy.orm import Session
from app.db.models.gym_machines import Gym_Machine
from fastapi import HTTPException

# CREATE
def createGymMachineService(db: Session, g_id: int, m_id: int, qty: int = 1):

    exist = db.query(Gym_Machine).filter(
        Gym_Machine.g_id == g_id,
        Gym_Machine.m_id == m_id
    ).first()

    if exist:
        raise HTTPException(
            status_code=400,
            detail="이미 등록된 기구입니다"
        )

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
        raise HTTPException(status_code=400)


# UPDATE
def updateGymMachineService(db: Session, g_id: int, m_id: int, qty: int):

    obj = db.query(Gym_Machine).filter(
        Gym_Machine.g_id == g_id,
        Gym_Machine.m_id == m_id
    ).first()

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="해당 기구가 존재하지 않습니다"
        )

    try:
        obj.qty = qty

        db.commit()
        db.refresh(obj)

        return obj

    except Exception:
        db.rollback()
        raise HTTPException(status_code=400)

# DELETE
def deleteGymMachineService(db: Session, g_id: int, m_id: int):

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
def getGymMachineService(db: Session, g_id: int):

    machines = (
        db.query(Gym_Machine)
        .filter(Gym_Machine.g_id == g_id)
        .all()
    )

    if not machines:
        raise HTTPException(status_code=404)

    return machines