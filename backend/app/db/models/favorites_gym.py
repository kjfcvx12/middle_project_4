from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint
from app.db.database import Base

class Favorite_Gym(Base):
    __tablename__ = "favorites_gym"

    id: Mapped[int] = mapped_column(primary_key=True)


    u_id: Mapped[int] = mapped_column(
        ForeignKey("users.u_id", ondelete="CASCADE")
    )
    gym_id: Mapped[int] = mapped_column(
        ForeignKey("gyms.gym_id", ondelete="CASCADE")
    )

    # 기존 유지 + back_populates만 추가
    user = relationship("User", back_populates="favorite_gyms")
    gym = relationship("Gym", back_populates="favorite_gyms")

    __table_args__ = (
        UniqueConstraint("u_id", "gym_id"),
    )