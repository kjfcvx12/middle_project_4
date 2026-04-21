from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .users import User
    from .machines import Machine


class Like_Machine(Base):
    __tablename__ = "like_machines"

    l_m_id: Mapped[int] = mapped_column(primary_key=True)
    
    # 외래키 설정
    u_id: Mapped[int] = mapped_column(ForeignKey("users.u_id", ondelete="set null"))
    m_id: Mapped[int] = mapped_column(ForeignKey("machines.m_id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="like_machines")
    machine: Mapped["Machine"] = relationship(back_populates="like_machines")

