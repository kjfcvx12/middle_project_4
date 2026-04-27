from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.db.crud import gyms as gym_crud
from app.db.scheme.gyms import GymCreate, GymUpdate


# CREATE
def services_gym_create(db: Session, data: GymCreate):
    try:
        gym = gym_crud.crud_gym_create(db, data)
        db.commit()
        db.refresh(gym)
        return gym

    except Exception:
        db.rollback()
        raise HTTPException(status_code=400)


# DETAIL
def services_gym_get(db: Session, g_id: int):
    try:
        gym = gym_crud.crud_gym_get(db, g_id)

        if not gym:
            raise HTTPException(status_code=404)

        return gym

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500)


# UPDATE
def services_gym_update(db: Session, g_id: int, data: GymUpdate):
    try:
        gym = gym_crud.crud_gym_get(db, g_id)

        if not gym:
            raise HTTPException(status_code=404)

        gym = gym_crud.crud_gym_update(db, gym, data)

        db.commit()
        db.refresh(gym)

        return gym

    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400)


# DELETE
def services_gym_delete(db: Session, g_id: int):
    try:
        gym = gym_crud.crud_gym_get(db, g_id)

        if not gym:
            raise HTTPException(status_code=404)

        gym_crud.crud_gym_delete(db, gym)

        db.commit()

        return True

    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500)


# LIST 
def services_gym_list(
    db: Session,
    skip: int,
    limit: int,
    name: str | None = None,
    address: str | None = None,
    sort: str | None = None
):
    try:
        gyms, total = gym_crud.crud_gyms_gets(
            db=db,
            skip=skip,
            limit=limit,
            name=name,
            address=address,
            sort=sort
        )

        return {
            "total": total,
            "page": (skip // limit) + 1,
            "size": limit,
            "data": gyms
        }

    except Exception:
        raise HTTPException(status_code=500)