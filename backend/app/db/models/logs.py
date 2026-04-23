from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from typing import TYPE_CHECKING, List
from app.db.database import Base

if TYPE_CHECKING:
    from app.db.models.log_details import Log_Detail
    from app.db.models.users import User
    from app.db.models.routines import Routine
    from app.db.models.machines import Machine

class Log(Base):
    __tablename__ = "logs"

    log_id: Mapped[int] = mapped_column(primary_key=True)

    # cascade 추가
    u_id: Mapped[int] = mapped_column(ForeignKey("users.u_id", ondelete="CASCADE"))
    r_id: Mapped[int] = mapped_column(ForeignKey("routines.r_id", ondelete="CASCADE"))
    m_id: Mapped[int] = mapped_column(ForeignKey("machines.m_id", ondelete="CASCADE"))

    log_date: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now()
    )

    attend: Mapped[bool] = mapped_column(default=False)

    # 핵심 수정 (delete → delete-orphan)
    details: Mapped[List["Log_Detail"]] = relationship(
        back_populates="log",
        cascade="all, delete-orphan"
    )

    user: Mapped["User"] = relationship("User", back_populates="log")
    routine: Mapped["Routine"] = relationship("Routine", back_populates="log")
    machine: Mapped["Machine"] = relationship("Machine", back_populates="log")