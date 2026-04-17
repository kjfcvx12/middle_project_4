from app.db.models.favorites_gym import Favorite_Gym

# 조회 (유지)
def crud_get_favorites_gym(db, user_id):
    return db.query(Favorite_Gym).filter(
        Favorite_Gym.u_id == user_id
    ).all()


# 삭제 (선택 유지)
def crud_delete_favorite_gym(db, user_id, gym_id):
    fav = db.query(Favorite_Gym).filter(
        Favorite_Gym.u_id == user_id,
        Favorite_Gym.gym_id == gym_id
    ).first()

    if fav:
        db.delete(fav)
        db.commit()


#  토글
def crud_toggle_favorite_gym(db, user_id, gym_id):
    fav = db.query(Favorite_Gym).filter(
        Favorite_Gym.u_id == user_id,
        Favorite_Gym.gym_id == gym_id
    ).first()

    if fav:
        db.delete(fav)
        db.commit()
        return {"status": "removed"}
    else:
        new_fav = Favorite_Gym(u_id=user_id, gym_id=gym_id)
        db.add(new_fav)
        db.commit()
        return {"status": "added"}