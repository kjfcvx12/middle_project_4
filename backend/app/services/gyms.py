from sqlalchemy.orm import Session
from app.db.crud import gyms as gym_crud
from app.db.scheme.gyms import GymCreate, GymUpdate
from app.db.models.users import User
from sqlalchemy.orm import Session
from app.db.models.gyms import Gym
from app.services import gym_staffs as gym_staff_service
from app.services import gym_machines as gym_machine_service

def createGymService(db: Session, data: GymCreate):
    gym = gym_crud.create_gym(db, data)

    db.commit()
    db.refresh(gym)

    return gym

def getGymService(db: Session, g_id: int):
    return gym_crud.get_gym(db, g_id)

def updateGymService(db: Session, g_id: int, data: GymUpdate):
    gym = gym_crud.get_gym(db, g_id)

    if not gym:
        return None

    gym = gym_crud.update_gym(db, gym, data)

    db.commit()
    db.refresh(gym)

    return gym

def deleteGymService(db: Session, g_id: int):
    gym = gym_crud.get_gym(db, g_id)

    if not gym:
        return False

    gym_crud.delete_gym(db, gym)

    db.commit()

    return True

def listGymService(
    db: Session,
    skip: int,
    limit: int,
    name: str | None = None,
    address: str | None = None,
    sort: str | None = None
):
    query = db.query(Gym)

    if name:
        query = query.filter(Gym.g_name.contains(name))

    if address:
        query = query.filter(Gym.g_addr.contains(address))

    total = query.count()

    if sort == "g_name,asc":
        query = query.order_by(Gym.g_name.asc())

    elif sort == "g_id,desc":
        query = query.order_by(Gym.g_id.desc())

    elif sort == "like_count,desc":
        query = query.order_by(Gym.g_id.desc())  # 현재 Gym 테이블만 쓰고 있어서 다른 테이블 기반 집계/정렬 안 됨 (like_gyms 테이블)

    elif sort == "favorite_count,desc":
        query = query.order_by(Gym.g_id.desc())  # 위와 동일 (favorite_gyms 테이블)

    else:
        query = query.order_by(Gym.g_id.desc())

    gyms = query.offset(skip).limit(limit).all()

    return gyms, total

def searchGymService(db: Session, name: str | None, address: str | None):
    return gym_crud.search_gyms(db, name, address)

def getGymTrainerService(db: Session, g_id: int):
    return gym_staff_service.getGymStaffService(db, g_id)

def getGymMachinesService(db: Session, g_id: int):
    return gym_machine_service.getGymMachineService(db, g_id)