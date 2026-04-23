from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import String, TIMESTAMP, func, ForeignKey
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .parts import Part

class Machine(Base):
    __tablename__ = "machines"
    m_id:Mapped[int]=mapped_column(primary_key=True)
    m_name:Mapped[str]=mapped_column(String(100), nullable=False)
    dsc:Mapped[str]=mapped_column(String(200), nullable=True)
    m_url:Mapped[str]=mapped_column(String(255))
    p_id:Mapped[Optional[int]]=mapped_column(ForeignKey('parts.p_id', ondelete="SET NULL"))
    
    part:Mapped[Optional["Part"]]= relationship(back_populates="machines")