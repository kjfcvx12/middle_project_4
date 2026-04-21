from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import  ForeignKey, UniqueConstraint
from users import User
from routines import Routine

class Favorite_Routine(Base):
    __tablename__="favorite_routines"
    f_r_id : Mapped[int]=mapped_column(primary_key=True)
    u_id : Mapped[int]=mapped_column(ForeignKey('users.u_id'),nullable=False)
    r_id : Mapped[int]=mapped_column(ForeignKey('routines.r_id'))

    user: Mapped["User"] = relationship(back_populates="favorite_routines")
    routine: Mapped["Routine"] = relationship(back_populates="favorite_routines")


    # 중복 방지
    __table_args__ = (
        UniqueConstraint("u_id", "r_id"),
    )