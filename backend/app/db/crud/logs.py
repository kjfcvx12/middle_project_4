from app.db.models.logs import Log
from app.db.models.log_details import LogDetail

# 생성 (log + detail 같이)
def crud_create_log(db, user_id, data):
    log = Log(
        u_id=user_id,
        r_id=data["r_id"],
        m_id=data["m_id"],
        attend=data["attend"]
    )
    db.add(log)
    db.commit()
    db.refresh(log)

    # detail 생성
    for d in data["details"]:
        detail = LogDetail(
            log_id=log.log_id,
            sets=d["sets"],
            reps=d["reps"],
            fail_memo=d.get("fail_memo"),
            memo=d["memo"]
        )
        db.add(detail)

    db.commit()
    return log


# 조회
def crud_get_logs(db, user_id):
    return db.query(Log).filter(Log.u_id == user_id).all()


# 삭제
def crud_delete_log(db, user_id, log_id):
    log = db.query(Log).filter(
        Log.u_id == user_id,
        Log.log_id == log_id
    ).first()

    if log:
        db.delete(log)
        db.commit()