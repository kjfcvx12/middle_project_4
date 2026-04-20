from app.db.models.favorites_machine import Favorite_Machine

# 조회 (유지)
def crud_get_favorites_machine(db, user_id):
    return db.query(Favorite_Machine).filter(
        Favorite_Machine.u_id == user_id
    ).all()


# 삭제 (선택 유지)
def crud_delete_favorite_machine(db, user_id, m_id):
    fav = db.query(Favorite_Machine).filter(
        Favorite_Machine.u_id == user_id,
        Favorite_Machine.m_id == m_id
    ).first()

    if fav:
        db.delete(fav)
        db.commit()


#  토글
def crud_toggle_favorite_machine(db, user_id, m_id):
    fav = db.query(Favorite_Machine).filter(
        Favorite_Machine.u_id == user_id,
        Favorite_Machine.m_id == m_id
    ).first()

    if fav:
        db.delete(fav)
        db.commit()
        return {"status": "removed"}
    else:
        new_fav = Favorite_Machine(u_id=user_id, m_id=m_id)
        db.add(new_fav)
        db.commit()
        return {"status": "added"}