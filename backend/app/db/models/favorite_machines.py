from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint
from typing import TYPE_CHECKING
from app.db.database import Base

if TYPE_CHECKING:
    from .users import User
    from .machines import Machine

class Favorite_Machine(Base):
    __tablename__ = "favorites_machine"

    f_m_id: Mapped[int] = mapped_column(primary_key=True)

    u_id: Mapped[int] = mapped_column(ForeignKey("users.u_id"))
    m_id: Mapped[int] = mapped_column(ForeignKey("machines.m_id"))

    # 관계
    user: Mapped["User"] = relationship(back_populates="favorites_machines")
    machine: Mapped["Machine"] = relationship(back_populates="favorites_machines")

    # 중복 방지
    __table_args__ = (
        UniqueConstraint("u_id", "m_id"),
    )