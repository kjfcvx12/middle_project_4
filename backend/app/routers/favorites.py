from fastapi import APIRouter, Depends
from app.services.favorites import *
from app.core.jwt_handle import get_current_user
from app.db.database import get_db

router = APIRouter(prefix="/favorites")

# -------- gym --------
@router.get("/gym")
def get_gym(db=Depends(get_db), user=Depends(get_current_user)):
    return service_get_favorites_gym(db, user)

@router.post("/gym/{gym_id}/toggle")
def toggle_gym(gym_id: int, db=Depends(get_db), user=Depends(get_current_user)):
    return service_toggle_favorite_gym(db, user, gym_id)

@router.delete("/gym/{gym_id}")
def delete_gym(gym_id: int, db=Depends(get_db), user=Depends(get_current_user)):
    return service_delete_favorite_gym(db, user, gym_id)


# -------- machine --------
@router.get("/machine")
def get_machine(db=Depends(get_db), user=Depends(get_current_user)):
    return service_get_favorites_machine(db, user)

@router.post("/machine/{m_id}/toggle")
def toggle_machine(m_id: int, db=Depends(get_db), user=Depends(get_current_user)):
    return service_toggle_favorite_machine(db, user, m_id)

@router.delete("/machine/{m_id}")
def delete_machine(m_id: int, db=Depends(get_db), user=Depends(get_current_user)):
    return service_delete_favorite_machine(db, user, m_id)


# -------- routine --------
@router.get("/routine")
def get_routine(db=Depends(get_db), user=Depends(get_current_user)):
    return service_get_favorites_routine(db, user)

@router.post("/routine/{r_id}/toggle")
def toggle_routine(r_id: int, db=Depends(get_db), user=Depends(get_current_user)):
    return service_toggle_favorite_routine(db, user, r_id)

@router.delete("/routine/{r_id}")
def delete_routine(r_id: int, db=Depends(get_db), user=Depends(get_current_user)):
    return service_delete_favorite_routine(db, user, r_id)