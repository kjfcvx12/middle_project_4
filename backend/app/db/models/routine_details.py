from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import String, TIMESTAMP, func, ForeignKey
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .routines import Routine
    from .machines import Machine

class Routine_Detail(Base):
    __tablename__="routine_details"
    r_d_id:Mapped[int]=mapped_column(primary_key=True)
    r_id:Mapped[int]=mapped_column(ForeignKey('routines.r_id', ondelete="CASCADE"))
    m_id:Mapped[int]=mapped_column(ForeignKey('machines.m_id'))
    step:Mapped[int]=mapped_column(nullable=False)
    sets:Mapped[int]=mapped_column(nullable=False)
    reps:Mapped[int]=mapped_column(nullable=False)
    rest_time: Mapped[Optional[int]] = mapped_column(nullable=True)

    routine:Mapped["Routine"]=relationship("Routine", back_populates="routine_details")
    machine:Mapped["Machine"]=relationship("Machine", back_populates="routine_details")
