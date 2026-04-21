from sqlalchemy.orm import Session
from app.db.models.gym_staffs import Gym_Staff

# CREATE
def createGymStaffService(db: Session, g_id: int, u_id: int):

    exist = db.query(Gym_Staff).filter(
        Gym_Staff.g_id == g_id,
        Gym_Staff.u_id == u_id
    ).first()

    if exist:
        return None

    obj = Gym_Staff(
        g_id=g_id,
        u_id=u_id
    )

    try:
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    except Exception:
        db.rollback()
        return None

# DELETE
def deleteGymStaffService(db: Session, g_id: int, u_id: int):

    obj = db.query(Gym_Staff).filter(
        Gym_Staff.g_id == g_id,
        Gym_Staff.u_id == u_id
    ).first()

    if not obj:
        return None

    try:
        db.delete(obj)
        db.commit()
        return True

    except Exception:
        db.rollback()
        return False

# LIST (옵션 - 트레이너 조회용)
def getGymStaffService(db: Session, g_id: int):

    return (
        db.query(Gym_Staff)
        .filter(Gym_Staff.g_id == g_id)
        .all()
    )