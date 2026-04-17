from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from typing import TYPE_CHECKING, List
from app.db.database import Base

if TYPE_CHECKING:
    from app.db.models.log_details import LogDetail
    from app.db.models.users import User
    from app.db.models.routines import Routine
    from app.db.models.machines import Machine

class Log(Base):
    __tablename__ = "logs"

    log_id: Mapped[int] = mapped_column(primary_key=True)

    u_id: Mapped[int] = mapped_column(ForeignKey("users.u_id"))
    r_id: Mapped[int] = mapped_column(ForeignKey("routines.r_id"))
    m_id: Mapped[int] = mapped_column(ForeignKey("machines.m_id"))

    log_date: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now()
    )

    attend: Mapped[bool] = mapped_column(default=False)

    # 관계
    details: Mapped[List["LogDetail"]] = relationship(
        back_populates="log",
        cascade="all, delete"
    )

    user: Mapped["User"] = relationship()
    routine: Mapped["Routine"] = relationship()
    machine: Mapped["Machine"] = relationship()