from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint
from typing import TYPE_CHECKING
from app.db.database import Base

if TYPE_CHECKING:
    from app.db.models.users import User
    from app.db.models.machines import Machine

class Favorite_Machine(Base):
    __tablename__ = "favorites_machine"

    id: Mapped[int] = mapped_column(primary_key=True)

    u_id = mapped_column(ForeignKey("users.u_id", ondelete="CASCADE"))
    m_id = mapped_column(ForeignKey("machines.m_id", ondelete="CASCADE"))

    # 관계
    user = relationship("User", back_populates="favorite_machines")
    machine = relationship("Machine", back_populates="favorite_machines")

    # 중복 방지
    __table_args__ = (
        UniqueConstraint("u_id", "m_id"),
    )