from sqlalchemy.orm import Session
from app.db.models.gym_staffs import Gym_Staff
from fastapi import HTTPException

# CREATE
def createGymStaffService(db: Session, g_id: int, u_id: int):

    exist = db.query(Gym_Staff).filter(
        Gym_Staff.g_id == g_id,
        Gym_Staff.u_id == u_id
    ).first()

    if exist:
        raise HTTPException(status_code=400)

    try:
        obj = Gym_Staff(
            g_id=g_id,
            u_id=u_id
        )

        db.add(obj)
        db.commit()
        db.refresh(obj)

        return obj

    except Exception:
        db.rollback()
        raise HTTPException(status_code=400)

# DELETE
def deleteGymStaffService(db: Session, g_id: int, u_id: int):

    obj = db.query(Gym_Staff).filter(
        Gym_Staff.g_id == g_id,
        Gym_Staff.u_id == u_id
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

# LIST (옵션 - 트레이너 조회용)
def getGymStaffService(db: Session, g_id: int):

    staff_list = (
        db.query(Gym_Staff)
        .filter(Gym_Staff.g_id == g_id)
        .all()
    )

    if not staff_list:
        raise HTTPException(status_code=404)

    return staff_list