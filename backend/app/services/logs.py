from app.db.crud.logs import create_log, get_logs

def create_log_service(db, user, data):
    return create_log(db, user.u_id, data)

def get_logs_service(db, user):
    return get_logs(db, user.u_id)