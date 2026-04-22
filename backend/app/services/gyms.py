from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.db.crud import gyms as gym_crud
from app.db.scheme.gyms import GymCreate, GymUpdate
from app.db.models.gyms import Gym


def services_gym_create(db: Session, data: GymCreate):
    try:
        gym = gym_crud.crud_gym_create(db, data)
        return gym

    except Exception as e:
        raise HTTPException(status_code=400)


def services_gym_service_get(db: Session, g_id: int):
    try:
        gym = gym_crud.crud_gym_get(db, g_id)

        if not gym:
            raise HTTPException(status_code=404)

        return gym

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500)


def services_gym_update(db: Session, g_id: int, data: GymUpdate):
    try:
        gym = gym_crud.crud_gym_get(db, g_id)

        if not gym:
            raise HTTPException(status_code=404, detail="헬스장 없음")

        updated_gym = gym_crud.crud_gym_update(db, gym, data)

        return updated_gym

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400)


def services_gym_delete(db: Session, g_id: int):
    try:
        gym = gym_crud.crud_gym_get(db, g_id)

        if not gym:
            raise HTTPException(status_code=404)

        gym_crud.crud_gym_delete(db, gym)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500)


def services_gym_list(
    db: Session,
    skip: int,
    limit: int,
    name: str | None = None,
    address: str | None = None,
    sort: str | None = None
):
    try:
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
            query = query.order_by(Gym.g_id.desc())

        elif sort == "favorite_count,desc":
            query = query.order_by(Gym.g_id.desc())

        else:
            query = query.order_by(Gym.g_id.desc())

        gyms = query.offset(skip).limit(limit).all()

        return gyms, total

    except Exception as e:
        raise HTTPException(status_code=500)


def services_gym_search(db: Session, name: str | None, address: str | None):
    try:
        return gym_crud.crud_gyms_search(db, name, address)

    except Exception as e:
        raise HTTPException(status_code=500)