from sqlalchemy.orm import Session
from app.db.models.gyms import Gym
from app.db.scheme.gyms import GymCreate, GymUpdate


# CREATE
def crud_gym_create(db: Session, data: GymCreate) -> Gym:
    gym = Gym(**data.model_dump())
    db.add(gym)
    db.flush()
    return gym


# READ
def crud_gym_get(db: Session, g_id: int):
    return db.query(Gym).filter(Gym.g_id == g_id).first()


# UPDATE
def crud_gym_update(db: Session, gym: Gym, data: GymUpdate):
    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(gym, key, value)

    db.flush()
    return gym


# DELETE
def crud_gym_delete(db: Session, gym: Gym):
    db.delete(gym)
    db.flush()


# LIST
def crud_gyms_gets(
    db: Session,
    skip: int,
    limit: int,
    name: str | None = None,
    address: str | None = None,
    sort: str | None = None
):
    query = db.query(Gym)

    if name:
        query = query.filter(Gym.g_name.contains(name))
    if address:
        query = query.filter(Gym.g_addr.contains(address))

    total = query.count()

    if sort == "g_name,asc":
        query = query.order_by(Gym.g_name.asc())
    elif sort == "g_id,desc":
        query = query.order_by(Gym.g_id.desc())
    elif sort == "like_count,desc":
        query = query.order_by(Gym.g_id.desc())
    elif sort == "favorite_count,desc":
        query = query.order_by(Gym.g_id.desc())
    else:
        query = query.order_by(Gym.g_id.desc())

    gyms = query.offset(skip).limit(limit).all()

    return gyms, total


# SEARCH
def crud_gyms_search(db: Session, name: str | None, address: str | None):
    query = db.query(Gym)

    if name:
        query = query.filter(Gym.g_name.contains(name))
    if address:
        query = query.filter(Gym.g_addr.contains(address))

    return query.all()