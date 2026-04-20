from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .users import User
    from .gyms import Gym


class Like_Gym(Base):
    __tablename__ = "like_gyms"

    l_g_id: Mapped[int] = mapped_column(primary_key=True)
    
    # 외래키 설정
    u_id: Mapped[int] = mapped_column(ForeignKey("users.u_id", ondelete="SET NULL"))
    g_id: Mapped[int] = mapped_column(ForeignKey("gyms.g_id"), nullable=False)
   
    user: Mapped["User"] = relationship(back_populates="like_gyms")
    gym: Mapped["Gym"] = relationship(back_populates="like_gyms")

