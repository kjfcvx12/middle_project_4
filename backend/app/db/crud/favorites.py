from app.models.favorites import Favorite

def add_favorite(db, user_id, log_id):
    fav = Favorite(u_id=user_id, log_id=log_id)
    db.add(fav)
    db.commit()
    return fav

def get_favorites(db, user_id):
    return db.query(Favorite).filter(Favorite.u_id == user_id).all()

def delete_favorite(db, user_id, log_id):
    fav = db.query(Favorite).filter(
        Favorite.u_id == user_id,
        Favorite.log_id == log_id
    ).first()

    if fav:
        db.delete(fav)
        db.commit()