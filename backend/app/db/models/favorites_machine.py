from sqlalchemy import Column, Integer, ForeignKey
from app.db.database import Base

class FavoriteMachine(Base):
    __tablename__ = "favorites_machine"

    id = Column(Integer, primary_key=True)
    u_id = Column(Integer, ForeignKey("users.u_id"))
    m_id = Column(Integer, ForeignKey("machines.m_id"))