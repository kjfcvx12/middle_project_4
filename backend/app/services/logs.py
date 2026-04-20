from app.db.crud.logs import *
from app.db.crud.log_detail import *

# 로그 + 디테일 생성
def service_create_log(db, user, data):

    log = crud_create_log(db, user.u_id, data)

    # detail 생성
    crud_create_log_details(db, log.log_id, data.details)

    try:
        db.commit()
    except:
        db.rollback()
        raise

    return log


def service_get_logs(db, user):
    return crud_get_logs(db, user.u_id)


def service_delete_log(db, user, log_id):
    result = crud_delete_log(db, user.u_id, log_id)

    try:
        db.commit()
    except:
        db.rollback()
        raise

    return {"msg": "삭제 완료"} if result else {"msg": "없음"}