from app.db.database import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, TIMESTAMP, func
from datetime import datetime
from typing import Optional



class User(Base):
    __tablename__ = "users"

    u_id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    pw: Mapped[str] = mapped_column(String(255), nullable=False)
    u_name: Mapped[str] = mapped_column(String(50), nullable=False)
    phone:  Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    role: Mapped[str] = mapped_column(String(50), nullable=False, default='user')
    # user|trainer|manager|admin

    signup_date: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    info: Mapped[Optional[str]] = mapped_column(String(255))

    refresh_token: Mapped[Optional[str]] = mapped_column(String(255))



    # routines : Mapped[list["Routine"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    # logs : Mapped[list["Log"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    # favorites : Mapped[list["Favorite"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    # boards : Mapped[list["Board"]] = relationship(back_populates="user")
    # comments : Mapped[list["Comment"]] = relationship(back_populates="user")

    # like_gyms : Mapped[list["Like_Gym"]] = relationship(back_populates="user")
    # like_machines : Mapped[list["Like_Machine"]] = relationship(back_populates="user")
    # like_routines : Mapped[list["Like_Routine"]] = relationship(back_populates="user")
    # like_boards : Mapped[list["Like_Board"]] = relationship(back_populates="user")

    # gym_staffs : Mapped["Gym_Staff"] = relationship(back_populates="user", cascade="all, delete-orphan", uselist=False)
