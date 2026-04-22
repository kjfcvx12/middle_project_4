from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.db.models.gym_machines import Gym_Machine
from app.db.crud import gym_machines as gym_machine_crud


# CREATE
def services_gym_machine_create(db: Session, g_id: int, m_id: int, qty: int = 1):
    try:
        exist = gym_machine_crud.crud_gym_machine_get(db, g_id, m_id)

        if exist:
            raise HTTPException(status_code=400)

        obj = Gym_Machine(g_id=g_id, m_id=m_id, qty=qty)
        return gym_machine_crud.crud_gym_machine_create(db, obj)

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500)


# UPDATE
def services_gym_machine_update(db: Session, g_id: int, m_id: int, qty: int):
    try:
        obj = gym_machine_crud.crud_gym_machine_get(db, g_id, m_id)

        if not obj:
            raise HTTPException(status_code=404)

        return gym_machine_crud.crud_gym_machine_update(db, obj, qty)

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500)


# DELETE
def services_gym_machine_delete(db: Session, g_id: int, m_id: int):
    try:
        obj = gym_machine_crud.crud_gym_machine_get(db, g_id, m_id)

        if not obj:
            raise HTTPException(status_code=404)

        gym_machine_crud.crud_gym_machine_delete(db, obj)

        return True

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500)


# LIST
def services_gym_machine_get(db: Session, g_id: int):
    try:
        machines = gym_machine_crud.crud_gym_machines_get_id(db, g_id)

        if not machines:
            raise HTTPException(status_code=404)

        return machines

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500)