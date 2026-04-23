from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint
from typing import TYPE_CHECKING
from app.db.database import Base

if TYPE_CHECKING:
    from app.db.models.users import User
    from app.db.models.gyms import Gym

class Favorite_Gym(Base):
    __tablename__ = "favorite_gyms"

    f_g_id: Mapped[int] = mapped_column(primary_key=True)

    u_id: Mapped[int] = mapped_column(ForeignKey("users.u_id"))
    g_id: Mapped[int] = mapped_column(ForeignKey("gyms.g_id"))

    # 관계
    user: Mapped["User"] = relationship(back_populates="favorite_gyms")
    gym: Mapped["Gym"] = relationship(back_populates="favorite_gyms")

    # 중복 방지
    __table_args__ = (
        UniqueConstraint("u_id", "g_id", name="uq_user_favorite_gym"),
    )