from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import String, TIMESTAMP, func, ForeignKey
from typing import Optional
from parts import Part

class Machine(Base):
    __tablename__ = "machines"
    m_id:Mapped[int]=mapped_column(primary_key=True)
    m_name:Mapped[str]=mapped_column(String(100), nullable=False)
    dsc:Mapped[str]=mapped_column(String(200), nullable=False)
    m_url:Mapped[str]=mapped_column(String(255))
    p_id:Mapped[int]=mapped_column(ForeignKey('parts.p_id'), nullable=False)
    
    part:Mapped["Part"]= relationship("Part",back_populates="parts")