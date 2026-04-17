from app.db.models.favorites_routine import Favorite_Routine

def crud_get_favorites_routine(db, user_id):
    return db.query(Favorite_Routine).filter(
        Favorite_Routine.u_id == user_id
    ).all()


def crud_delete_favorite_routine(db, user_id, r_id):
    fav = db.query(Favorite_Routine).filter(
        Favorite_Routine.u_id == user_id,
        Favorite_Routine.r_id == r_id
    ).first()

    if fav:
        db.delete(fav)
        db.commit()


def crud_toggle_favorite_routine(db, user_id, r_id):
    fav = db.query(Favorite_Routine).filter(
        Favorite_Routine.u_id == user_id,
        Favorite_Routine.r_id == r_id
    ).first()

    if fav:
        db.delete(fav)
        db.commit()
        return {"status": "removed"}
    else:
        new_fav = Favorite_Routine(u_id=user_id, r_id=r_id)
        db.add(new_fav)
        db.commit()
        return {"status": "added"}