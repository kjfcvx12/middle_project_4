from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, TIMESTAMP, func
from datetime import datetime
from typing import Optional


class User(Base):
    __tablename__="users"


    u_id:Mapped[int]=mapped_column(primary_key=True)
    email:Mapped[str]=mapped_column(String(100), nullable=False, unique=True)
    pw:Mapped[str]=mapped_column(String(255), nullable=False, unique=True)
    u_name:Mapped[str]=mapped_column(String(50), nullable=False)
    refresh_token:Mapped[Optional[str]]=mapped_column(String(255))
    signup_date:Mapped[datetime]=mapped_column(TIMESTAMP, server_default=func.now())
    info:Mapped[Optional[str]]=mapped_column(String(255))
