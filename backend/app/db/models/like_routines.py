from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .users import User
    from .routines import Routine

class Like_Routine(Base):
    __tablename__="like_routines"
    l_r_id:Mapped[int]=mapped_column(primary_key=True)
    u_id:Mapped[int]=mapped_column(ForeignKey("users.u_id"), nullable=False)
    r_id:Mapped[int]=mapped_column(ForeignKey("routines.r_id"), nullable=False)

    user:Mapped["User"]= relationship("User", back_populates="like_routines")
    routine:Mapped["Routine"]= relationship("Routine", back_populates="like_routines")