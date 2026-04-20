from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint
from typing import TYPE_CHECKING
from app.db.database import Base

if TYPE_CHECKING:
    from app.db.models.users import User
    from app.db.models.routines import Routine

class Favorite_Routine(Base):
    __tablename__ = "favorites_routine"

    id: Mapped[int] = mapped_column(primary_key=True)

    u_id: Mapped[int] = mapped_column(ForeignKey("users.u_id", ondelete="CASCADE"))
    r_id: Mapped[int] = mapped_column(ForeignKey("routines.r_id", ondelete="CASCADE"))

    # 관계
    user = relationship("User", back_populates="favorite_routines")
    routine = relationship("Routine", back_populates="favorite_routines")

    # 중복 방지
    __table_args__ = (
        UniqueConstraint("u_id", "r_id"),
    )