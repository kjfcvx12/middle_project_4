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
    from .favorite_routines import Favorite_Routine

    from .logs import Log

    from .boards import Board
    from .like_boards import Like_Board

    from .comments import Comment
    from .like_comments import Like_Comment

    from .gym_staffs import Gym_Staff




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


    # 유저 삭제시 전부 삭제
    routines : Mapped[list["Routine"]] = relationship("Routine", back_populates="user", cascade="all, delete-orphan")
    logs : Mapped[list["Log"]] = relationship("Log", back_populates="user", cascade="all, delete-orphan")
    
    favorite_gyms : Mapped[list["Favorite_Gym"]] = relationship("Favorite_Gym", back_populates="user", cascade="all, delete-orphan")
    favorite_machines : Mapped[list["Favorite_Machine"]] = relationship("Favorite_Machine", back_populates="user", cascade="all, delete-orphan")
    favorite_routines : Mapped[list["Favorite_Routine"]] = relationship("Favorite_Routine", back_populates="user", cascade="all, delete-orphan")


    # 유저 삭제시 유지
    boards : Mapped[list["Board"]] = relationship("Board", back_populates="user", passive_deletes=True)
    comments : Mapped[list["Comment"]] = relationship("Comment", back_populates="user", passive_deletes=True)

    like_gyms : Mapped[list["Like_Gym"]] = relationship("Like_Gym", back_populates="user", passive_deletes=True)
    like_machines : Mapped[list["Like_Machine"]] = relationship("Like_Machine", back_populates="user", passive_deletes=True)
    like_boards : Mapped[list["Like_Board"]] = relationship("Like_Board", back_populates="user", passive_deletes=True)
    like_comments : Mapped[list["Like_Comment"]] = relationship("Like_Comment", back_populates="user", passive_deletes=True)

    gym_staff : Mapped["Gym_Staff"] = relationship("Gym_Staff", back_populates="user", cascade="all, delete-orphan", uselist=False)

    # 쪽지용
    sent_notes: Mapped[list["Note"]] = relationship("Note", foreign_keys="Note.send_id", back_populates="sender", passive_deletes=True)
    received_notes: Mapped[list["Note"]] = relationship("Note", foreign_keys="Note.rece_id", back_populates="receiver", passive_deletes=True)