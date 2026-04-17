from app.models.logs import Log
from app.models.log_details import LogDetail

# log + detail 동시에 생성
def create_log(db, user_id, data):
    log = Log(
        u_id=user_id,
        r_id=data.r_id,
        m_id=data.m_id,
        attend=data.attend
    )
    db.add(log)
    db.commit()
    db.refresh(log)

    # detail 여러 개 생성
    for d in data.details:
        detail = LogDetail(
            log_id=log.log_id,
            sets=d.sets,
            reps=d.reps,
            fail_memo=d.fail_memo,
            memo=d.memo
        )
        db.add(detail)

    db.commit()
    return log


def get_logs(db, user_id):
    return db.query(Log).filter(Log.u_id == user_id).all()