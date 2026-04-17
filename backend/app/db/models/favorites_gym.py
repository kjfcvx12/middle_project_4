from sqlalchemy import Column, Integer, ForeignKey
from app.db.database import Base

class Favorite(Base):
    __tablename__ = "favorites"

    # PK 설정 
    id = Column(Integer, primary_key=True)

    # FK 설정
    u_id = Column(Integer, ForeignKey("users.u_id"))
    log_id = Column(Integer, ForeignKey("logs.log_id"))