from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class LogDetail(Base):
    __tablename__ = "log_details"

    # PK 설정 
    log_d_id = Column(Integer, primary_key=True)

    # FK 설정 
    log_id = Column(Integer, ForeignKey("logs.log_id"))

    # 세트 정보
    sets = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)

    # 메모
    fail_memo = Column(String(100))
    memo = Column(String(300), nullable=False)

    # 역참조
    log = relationship("Log", back_populates="details")