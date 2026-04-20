from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import  ForeignKey
from users import User
from routines import Routine

class Favorite_Routine(Base):
    __tablename__="favorite_routines"
    f_r_id : Mapped[int]=mapped_column(primary_key=True)
    u_id : Mapped[int]=mapped_column(ForeignKey('users.u_id'),nullable=False)
    r_id : Mapped[int]=mapped_column(ForeignKey('routines.r_id'))

    user: Mapped["User"] = relationship("User", back_populates="favorite_routines")
    routine: Mapped["Routine"] = relationship("Routine", back_populates="favorite_routines")