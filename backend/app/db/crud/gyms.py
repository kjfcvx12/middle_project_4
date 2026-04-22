from sqlalchemy.orm import Session
from app.db.models.gyms import Gym
from app.db.scheme.gyms import GymCreate, GymUpdate

# CREATE
def create_gym(db: Session, data: GymCreate) -> Gym:
    gym = Gym(**data.model_dump())
    db.add(gym)
    db.flush()
    return gym

# READ
def get_gym(db: Session, g_id: int):
    return db.query(Gym).filter(Gym.g_id == g_id).first()

# UPDATE
def update_gym(db: Session, gym: Gym, data: GymUpdate):
    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(gym, key, value)

    db.flush() 
    return gym

# DELETE
def delete_gym(db: Session, gym: Gym):
    db.delete(gym)
    db.flush()

# LIST
def get_gyms(db: Session, skip: int, limit: int):
    return db.query(Gym).offset(skip).limit(limit).all()

# SEARCH
def search_gyms(db: Session, name: str | None, address: str | None):
    query = db.query(Gym)

    if name:
        query = query.filter(Gym.g_name.contains(name))
    if address:
        query = query.filter(Gym.g_addr.contains(address))

    return query.all()