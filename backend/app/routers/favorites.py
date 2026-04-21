from fastapi import APIRouter, Depends, HTTPException
from app.services.favorites import *
from app.core.jwt_handle import get_current_user
from app.db.database import get_db
from app.db.scheme.favorites import (
    FavoriteGymCreate,
    FavoriteMachineCreate,
    FavoriteRoutineCreate
)

router = APIRouter()


# -------- gym --------

# 즐겨찾기 토글 (추가/삭제 자동 처리)
@router.post("/favorite_gyms")
def toggle_gym(data: FavoriteGymCreate, db=Depends(get_db), user=Depends(get_current_user)):
    return service_toggle_favorite_gym(db, user, data.gym_id)


# 즐겨찾기 삭제 (명세 유지용)
@router.delete("/favorite_gyms")
def delete_gym(data: FavoriteGymCreate, db=Depends(get_db), user=Depends(get_current_user)):
    return service_delete_favorite_gym(db, user, data.gym_id)


# 특정 유저 즐겨찾기 조회
@router.get("/users/favorite_gym/{u_id}")
def get_gym(u_id: int, db=Depends(get_db), user=Depends(get_current_user)):

    # 본인만 조회 가능 (보안)
    if user.u_id != u_id:
        raise HTTPException(status_code=403, detail="권한 없음")

    data = service_get_favorites_gym(db, u_id)

    # 명세에 맞게 응답 형태 변환
    return {
        "data": [
            {
                "g_id": f.gym.gym_id,
                "g_name": f.gym.g_name
            }
            for f in data
        ]
    }


# -------- machine --------

@router.post("/favorite_machines")
def toggle_machine(data: FavoriteMachineCreate, db=Depends(get_db), user=Depends(get_current_user)):
    return service_toggle_favorite_machine(db, user, data.m_id)


@router.delete("/favorite_machines")
def delete_machine(data: FavoriteMachineCreate, db=Depends(get_db), user=Depends(get_current_user)):
    return service_delete_favorite_machine(db, user, data.m_id)


@router.get("/users/favorite_machine/{u_id}")
def get_machine(u_id: int, db=Depends(get_db), user=Depends(get_current_user)):

    if user.u_id != u_id:
        raise HTTPException(status_code=403, detail="권한 없음")

    data = service_get_favorites_machine(db, u_id)

    return {
        "data": [
            {
                "m_id": f.machine.m_id,
                "m_name": f.machine.m_name
            }
            for f in data
        ]
    }


# -------- routine --------

@router.post("/favorite_routines")
def toggle_routine(data: FavoriteRoutineCreate, db=Depends(get_db), user=Depends(get_current_user)):
    return service_toggle_favorite_routine(db, user, data.r_id)


@router.delete("/favorite_routines")
def delete_routine(data: FavoriteRoutineCreate, db=Depends(get_db), user=Depends(get_current_user)):
    return service_delete_favorite_routine(db, user, data.r_id)


@router.get("/users/favorite_routines/{u_id}")
def get_routine(u_id: int, db=Depends(get_db), user=Depends(get_current_user)):

    if user.u_id != u_id:
        raise HTTPException(status_code=403, detail="권한 없음")

    data = service_get_favorites_routine(db, u_id)

    return {
        "data": [
            {
                "r_id": f.routine.r_id,
                "r_name": f.routine.r_name
            }
            for f in data
        ]
    }