from app.db.database import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, TIMESTAMP, func
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .notes import Note

    from .like_gyms import Like_Gym
    from .favorite_gyms import Favorite_Gym

    from .like_machines import Like_Machine
    from .favorite_machines import Favorite_Machine

    from .routines import Routine
    from .like_routines import Like_Routine
    from .favorite_routines import Favorite_Routine

    from .logs import Log

    from .boards import Board
    from .like_boards import Like_Board

    from .comments import Comment
    from .like_comments import Like_Comment




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
    
    favorite_gyms : Mapped[list["Favorite_Gym"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    favorite_machines : Mapped[list["Favorite_Machine"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    favorite_routines : Mapped[list["Favorite_Routine"]] = relationship(back_populates="user", cascade="all, delete-orphan")


    # boards : Mapped[list["Board"]] = relationship(back_populates="user")
    # comments : Mapped[list["Comment"]] = relationship(back_populates="user")

    like_gyms : Mapped[list["Like_Gym"]] = relationship(back_populates="user")
    like_machines : Mapped[list["Like_Machine"]] = relationship(back_populates="user")
    like_routines : Mapped[list["Like_Routine"]] = relationship(back_populates="user")
    like_boards : Mapped[list["Like_Board"]] = relationship(back_populates="user")

    # gym_staffs : Mapped["Gym_Staff"] = relationship(back_populates="user", cascade="all, delete-orphan", uselist=False)


    sent_notes: Mapped[list["Note"]] = relationship("Note", foreign_keys="[Note.send_id]", back_populates="sender")
    received_notes: Mapped[list["Note"]] = relationship("Note", foreign_keys="[Note.rece_id]", back_populates="receiver")