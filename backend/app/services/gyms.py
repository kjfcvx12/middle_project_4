from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.db.crud import gyms as gym_crud
from app.db.scheme.gyms import GymCreate, GymUpdate


async def services_gym_create(db: Session, data: GymCreate):
    try:
        result=gym_crud.crud_gym_create(db, data)

        await db.commit()
        await db.refresh(result)

        return result

    except Exception:
        await db.rollback()
        raise HTTPException(status_code=400)


async def services_gym_get(db: Session, g_id: int):
    try:
        gym = gym_crud.crud_gym_get(db, g_id)

        if not gym:
            raise HTTPException(status_code=404)

        return gym

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500)


async def services_gym_update(db: Session, g_id: int, data: GymUpdate):
    try:
        gym = gym_crud.crud_gym_get(db, g_id)

        if not gym:
            raise HTTPException(status_code=404)

        result=gym_crud.crud_gym_update(db, gym, data)

        await db.commit()
        await db.refresh(result)

        return result

    except HTTPException:
        raise
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=400)


async def services_gym_delete(db: Session, g_id: int):
    try:
        gym = gym_crud.crud_gym_get(db, g_id)

        if not gym:
            raise HTTPException(status_code=404)

        gym_crud.crud_gym_delete(db, gym)

        await db.commit()

    except HTTPException:
        raise
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500)


# LIST 
async def services_gym_list(
    db: Session,
    page:int,
    name: str | None = None,
    address: str | None = None,
    sort: str | None = None
):
    try:
        return gym_crud.crud_gyms_gets(
            db=db,
            page=page,   
            name=name,
            address=address,
            sort=sort
        )

    except Exception:
        raise HTTPException(status_code=500)


async def services_gym_search(db: Session, name: str | None, address: str | None):
    try:
        return gym_crud.crud_gyms_search(db, name, address)

    except Exception:
        raise HTTPException(status_code=500)