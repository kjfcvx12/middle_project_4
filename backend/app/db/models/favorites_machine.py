from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint
from typing import TYPE_CHECKING
from app.db.database import Base

if TYPE_CHECKING:
    from app.db.models.users import User
    from app.db.models.machines import Machine

class FavoriteMachine(Base):
    __tablename__ = "favorites_machine"

    id: Mapped[int] = mapped_column(primary_key=True)

    u_id: Mapped[int] = mapped_column(ForeignKey("users.u_id"))
    m_id: Mapped[int] = mapped_column(ForeignKey("machines.m_id"))

    user: Mapped["User"] = relationship()
    machine: Mapped["Machine"] = relationship()

    __table_args__ = (
        UniqueConstraint("u_id", "m_id"),
    )