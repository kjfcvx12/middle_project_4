from app.db.models.favorites_gym import Favorite_Gym

# 특정 유저의 즐겨찾기 조회
def crud_get_favorites_gym(db, user_id):
    return db.query(Favorite_Gym).filter(
        Favorite_Gym.u_id == user_id
    ).all()


# 즐겨찾기 삭제 (존재하면 삭제)
def crud_delete_favorite_gym(db, user_id, gym_id):
    fav = db.query(Favorite_Gym).filter(
        Favorite_Gym.u_id == user_id,
        Favorite_Gym.gym_id == gym_id
    ).first()

    if fav:
        db.delete(fav)   # DB에서 제거
        return True
    return False


# 즐겨찾기 토글 (있으면 삭제, 없으면 추가)
def crud_toggle_favorite_gym(db, user_id, gym_id):
    fav = db.query(Favorite_Gym).filter(
        Favorite_Gym.u_id == user_id,
        Favorite_Gym.gym_id == gym_id
    ).first()

    if fav:
        db.delete(fav)
        return "removed"   # 삭제됨
    else:
        new_fav = Favorite_Gym(u_id=user_id, gym_id=gym_id)
        db.add(new_fav)
        return "added"     # 추가됨