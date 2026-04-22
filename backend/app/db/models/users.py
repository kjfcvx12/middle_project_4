from app.db.database import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, TIMESTAMP, func, Enum
from datetime import datetime
from typing import Optional
import enum


class UserRole(str, enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class User(Base):
    __tablename__ = "users"

    u_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    pw: Mapped[str] = mapped_column(String(255), nullable=False)
    u_name: Mapped[str] = mapped_column(String(50), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, default=UserRole.USER)
    refresh_token: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    signup_date: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    info: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)