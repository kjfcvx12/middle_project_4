from sqlalchemy.orm import Session
from app.db.models.gyms import Gym
from app.db.scheme.gyms import GymCreate, GymUpdate

def createGym(db: Session, data: GymCreate) -> Gym:
    gym = Gym(**data.model_dump())
    db.add(gym)
    db.commit()
    db.refresh(gym)
    return gym

def getGym(db: Session, g_id: int):
    return db.query(Gym).filter(Gym.g_id == g_id).first()

def updateGym(db: Session, gym: Gym, data: GymUpdate):
    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(gym, key, value)

    db.commit()
    db.refresh(gym)
    return gym

def deleteGym(db: Session, gym: Gym):
    db.delete(gym)
    db.commit()

def getGyms(db: Session, skip: int, limit: int):
    return db.query(Gym).offset(skip).limit(limit).all()

def searchGyms(db: Session, name: str | None, address: str | None):
    query = db.query(Gym)

    if name:
        query = query.filter(Gym.g_name.contains(name))
    if address:
        query = query.filter(Gym.g_addr.contains(address))

    return query.all()