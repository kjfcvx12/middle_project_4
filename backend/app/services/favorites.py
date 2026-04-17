from app.db.crud.favorites_gym import *
from app.db.crud.favorites_machine import *
from app.db.crud.favorites_routine import *

# -------- gym --------
def service_get_favorites_gym(db, user):
    return crud_get_favorites_gym(db, user.u_id)

def service_delete_favorite_gym(db, user, gym_id):
    return crud_delete_favorite_gym(db, user.u_id, gym_id)

def service_toggle_favorite_gym(db, user, gym_id):
    return crud_toggle_favorite_gym(db, user.u_id, gym_id)


# -------- machine --------
def service_get_favorites_machine(db, user):
    return crud_get_favorites_machine(db, user.u_id)

def service_delete_favorite_machine(db, user, m_id):
    return crud_delete_favorite_machine(db, user.u_id, m_id)

def service_toggle_favorite_machine(db, user, m_id):
    return crud_toggle_favorite_machine(db, user.u_id, m_id)


# -------- routine --------
def service_get_favorites_routine(db, user):
    return crud_get_favorites_routine(db, user.u_id)

def service_delete_favorite_routine(db, user, r_id):
    return crud_delete_favorite_routine(db, user.u_id, r_id)

def service_toggle_favorite_routine(db, user, r_id):
    return crud_toggle_favorite_routine(db, user.u_id, r_id)