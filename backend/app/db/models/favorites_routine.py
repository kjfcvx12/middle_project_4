from sqlalchemy import Column, Integer, ForeignKey
from app.db.database import Base

class FavoriteRoutine(Base):
    __tablename__ = "favorites_routine"

    id = Column(Integer, primary_key=True)
    u_id = Column(Integer, ForeignKey("users.u_id"))
    r_id = Column(Integer, ForeignKey("routines.r_id"))