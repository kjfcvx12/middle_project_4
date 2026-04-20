from app.db.models.logs import Log

# 로그 생성 (detail 제외)
def crud_create_log(db, user_id, data):
    log = Log(
        u_id=user_id,
        r_id=data.r_id,
        m_id=data.m_id,
        attend=data.attend
    )
    db.add(log)
    db.flush()  # commit 대신 flush (id 확보용)

    return log


# 조회
def crud_get_logs(db, user_id):
    return db.query(Log).filter(Log.u_id == user_id).all()


# 삭제 (cascade로 detail 자동 삭제됨)
def crud_delete_log(db, user_id, log_id):
    log = db.query(Log).filter(
        Log.u_id == user_id,
        Log.log_id == log_id
    ).first()

    if log:
        db.delete(log)
        return True
    return False