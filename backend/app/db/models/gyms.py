from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .like_gyms import Like_Gym
    from .favorite_gyms import Favorite_Gym
    from .gym_staffs import Gym_Staff
    from .gym_machines import Gym_Machine


class Gym(Base):
    __tablename__ = "gyms"

    g_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    g_name: Mapped[str] = mapped_column(String(100), nullable=False)
    g_addr: Mapped[str] = mapped_column(String(255), nullable=False)
    g_tel: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    shower: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    parking: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    elev: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    open_time: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    like_gyms: Mapped[list["Like_Gym"]]=relationship("Like_Gym", back_populates="gym", cascade="all, delete-orphan")
    favorite_gyms: Mapped[list["Favorite_Gym"]] = relationship("Favorite_Gym", back_populates="gym", cascade="all, delete-orphan")
    gym_staffs:Mapped[list["Gym_Staff"]] = relationship("Gym_Staff",back_populates="gym", cascade="all, delete-orphan")
    gym_machines:Mapped[list["Gym_Machine"]] = relationship("Gym_Machine",back_populates="gym")
    



