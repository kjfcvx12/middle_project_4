from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import String, TIMESTAMP, func, ForeignKey
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .users import User
    from .parts import Part
    from .routine_details import Routine_Detail
    

class Routine(Base):
    __tablename__="routines"
    r_id:Mapped[int]=mapped_column(primary_key=True)
    r_name:Mapped[str]=mapped_column(String(100),nullable=False)
    u_id:Mapped[int]=mapped_column(ForeignKey('users.u_id'),nullable=True)
    p_id: Mapped[Optional[int]] = mapped_column(ForeignKey('parts.p_id'), nullable=True)

    user:Mapped["User"]=relationship("User",back_populates="routines")
    part:Mapped["Part"]=relationship("Part",back_populates="routines")
    routine_details: Mapped[list["Routine_Detail"]] = relationship(
    "Routine_Detail", back_populates="routine", cascade="all, delete-orphan")
       