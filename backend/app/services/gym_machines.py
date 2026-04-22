from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.db.models.gym_machines import Gym_Machine
from app.db.crud import gym_machines as gym_machine_crud


# CREATE
def services_gym_machine_create(db: Session, g_id: int, m_id: int, qty: int = 1):
    try:
        exist = db.query(Gym_Machine).filter(
            Gym_Machine.g_id == g_id,
            Gym_Machine.m_id == m_id
        ).first()

        if exist:
            raise HTTPException(status_code=400)

        obj = gym_machine_crud.crud_gym_machine_create(db, g_id, m_id, qty)
        return obj

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500)


# UPDATE
def services_gym_machine_update(db: Session, g_id: int, m_id: int, qty: int):
    try:
        obj = db.query(Gym_Machine).filter(
            Gym_Machine.g_id == g_id,
            Gym_Machine.m_id == m_id
        ).first()

        if not obj:
            raise HTTPException(status_code=404)

        updated = gym_machine_crud.crud_gym_machine_update(db, obj, qty)
        return updated

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500)


# DELETE
def services_gym_machine_delete(db: Session, g_id: int, m_id: int):
    try:
        obj = db.query(Gym_Machine).filter(
            Gym_Machine.g_id == g_id,
            Gym_Machine.m_id == m_id
        ).first()

        if not obj:
            raise HTTPException(status_code=404)

        gym_machine_crud.crud_gym_machine_delete(db, obj)

        return True

    except HTTPException:
        raise
    except Exception as e:
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
    except Exception as e:
        raise HTTPException(status_code=500)