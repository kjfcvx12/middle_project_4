from app.db.crud.favorites_gym import *
from app.db.crud.favorites_machine import *
from app.db.crud.favorites_routine import *


# -------- gym --------

# 즐겨찾기 조회
def service_get_favorites_gym(db, user_id):
    return crud_get_favorites_gym(db, user_id)


# 즐겨찾기 삭제
def service_delete_favorite_gym(db, user, gym_id):
    result = crud_delete_favorite_gym(db, user.u_id, gym_id)

    try:
        db.commit()   # 실제 DB 반영
    except:
        db.rollback() # 실패 시 되돌림
        raise

    if result:
        return {"msg": "즐겨찾기 취소"}
    return {"msg": "존재하지 않음"}


# 즐겨찾기 토글
def service_toggle_favorite_gym(db, user, gym_id):
    result = crud_toggle_favorite_gym(db, user.u_id, gym_id)

    try:
        db.commit()
    except:
        db.rollback()
        raise

    if result == "added":
        return {"msg": "즐겨찾기 등록"}
    else:
        return {"msg": "즐겨찾기 취소"}


# -------- machine --------

def service_get_favorites_machine(db, user_id):
    return crud_get_favorites_machine(db, user_id)


def service_delete_favorite_machine(db, user, m_id):
    result = crud_delete_favorite_machine(db, user.u_id, m_id)

    try:
        db.commit()
    except:
        db.rollback()
        raise

    if result:
        return {"msg": "즐겨찾기 취소"}
    return {"msg": "존재하지 않음"}


def service_toggle_favorite_machine(db, user, m_id):
    result = crud_toggle_favorite_machine(db, user.u_id, m_id)

    try:
        db.commit()
    except:
        db.rollback()
        raise

    if result == "added":
        return {"msg": "즐겨찾기 등록"}
    else:
        return {"msg": "즐겨찾기 취소"}


# -------- routine --------

def service_get_favorites_routine(db, user_id):
    return crud_get_favorites_routine(db, user_id)


def service_delete_favorite_routine(db, user, r_id):
    result = crud_delete_favorite_routine(db, user.u_id, r_id)

    try:
        db.commit()
    except:
        db.rollback()
        raise

    if result:
        return {"msg": "즐겨찾기 취소"}
    return {"msg": "존재하지 않음"}


def service_toggle_favorite_routine(db, user, r_id):
    result = crud_toggle_favorite_routine(db, user.u_id, r_id)

    try:
        db.commit()
    except:
        db.rollback()
        raise

    if result == "added":
        return {"msg": "즐겨찾기 등록"}
    else:
        return {"msg": "즐겨찾기 취소"}