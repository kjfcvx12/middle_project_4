from app.db.crud.logs import *

def service_create_log(db, user, data):
    return crud_create_log(db, user.u_id, data)

def service_get_logs(db, user):
    return crud_get_logs(db, user.u_id)

def service_delete_log(db, user, log_id):
    return crud_delete_log(db, user.u_id, log_id)