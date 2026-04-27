from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .users import User
    from .gyms import Gym

class Gym_Staff(Base):
    __tablename__ = "gym_staffs"

    g_s_id: Mapped[int] = mapped_column(primary_key=True)

    g_id: Mapped[int] = mapped_column(ForeignKey("gyms.g_id", ondelete="SET NULL"), nullable=True)
    u_id: Mapped[int] = mapped_column(ForeignKey("users.u_id"), unique=True)

    user: Mapped["User"] = relationship("User", back_populates="gym_staff")
    gym: Mapped["Gym"]= relationship("Gym", back_populates="gym_staffs")