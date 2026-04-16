from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from machines import Machine

class Like(Base):
    __tablename__="like_machines"

    lm_id:Mapped[int]=mapped_column(primary_key=True)
    user_id:Mapped[int]=mapped_column(ForeignKey("users.u_id"))
    m_id:Mapped[int]=mapped_column(ForeignKey("machines.m_id"), nullable=False)

    machine:Mapped["Machine"]=relationship("Machine", back_populates="like_machines")