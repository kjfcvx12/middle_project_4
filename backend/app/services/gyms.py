from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.db.crud import gyms as gym_crud
from app.db.scheme.gyms import Gym_Create, Gym_Update


<<<<<<< HEAD
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
=======
async def services_gym_create(db: Session, data: Gym_Create):
    try:
        result=gym_crud.crud_gym_create(db, data)

        await db.commit()
        await db.refresh(result)

        return result

    except Exception:
        await db.rollback()
        raise HTTPException(status_code=400)


async def services_gym_get(db: Session, g_id: int):
>>>>>>> 58e719c560343188a154edfc7bbb003500c69f21
    try:
        gym = gym_crud.crud_gym_get(db, g_id)

        if not gym:
            raise HTTPException(status_code=404)

        return gym

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500)


<<<<<<< HEAD
# UPDATE
def services_gym_update(db: Session, g_id: int, data: GymUpdate):
=======
async def services_gym_update(db: Session, g_id: int, data: Gym_Update):
>>>>>>> 58e719c560343188a154edfc7bbb003500c69f21
    try:
        gym = gym_crud.crud_gym_get(db, g_id)

        if not gym:
            raise HTTPException(status_code=404)

<<<<<<< HEAD
        gym = gym_crud.crud_gym_update(db, gym, data)

        db.commit()
        db.refresh(gym)

        return gym
=======
        result=gym_crud.crud_gym_update(db, gym, data)

        await db.commit()
        await db.refresh(result)

        return result
>>>>>>> 58e719c560343188a154edfc7bbb003500c69f21

    except HTTPException:
        raise
    except Exception:
<<<<<<< HEAD
        db.rollback()
=======
        await db.rollback()
>>>>>>> 58e719c560343188a154edfc7bbb003500c69f21
        raise HTTPException(status_code=400)


# DELETE
def services_gym_delete(db: Session, g_id: int):
    try:
        gym = gym_crud.crud_gym_get(db, g_id)

        if not gym:
            raise HTTPException(status_code=404)

        gym_crud.crud_gym_delete(db, gym)

<<<<<<< HEAD
        db.commit()

        return True
=======
        await db.commit()
>>>>>>> 58e719c560343188a154edfc7bbb003500c69f21

    except HTTPException:
        raise
    except Exception:
<<<<<<< HEAD
        db.rollback()
=======
        await db.rollback()
>>>>>>> 58e719c560343188a154edfc7bbb003500c69f21
        raise HTTPException(status_code=500)


# LIST 
def services_gym_list(
    db: Session,
<<<<<<< HEAD
    skip: int,
    limit: int,
=======
    page:int,
>>>>>>> 58e719c560343188a154edfc7bbb003500c69f21
    name: str | None = None,
    address: str | None = None,
    sort: str | None = None
):
    try:
        gyms, total = gym_crud.crud_gyms_gets(
            db=db,
<<<<<<< HEAD
            skip=skip,
            limit=limit,
=======
            page=page,   
>>>>>>> 58e719c560343188a154edfc7bbb003500c69f21
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