from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base

class Log(Base):
    __tablename__ = "logs"

    # PK 설정
    log_id = Column(Integer, primary_key=True)

    # FK 설정
    u_id = Column(Integer, ForeignKey("users.u_id"))
    r_id = Column(Integer, ForeignKey("routines.r_id"))
    m_id = Column(Integer, ForeignKey("machines.m_id"))

    # 운동 날짜
    log_date = Column(DateTime, server_default=func.now())

    # 출석 여부
    attend = Column(Boolean, default=False)

    # log_detail 관계
    details = relationship("LogDetail", back_populates="log", cascade="all, delete")