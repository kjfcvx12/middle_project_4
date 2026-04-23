from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import String, TIMESTAMP, func, ForeignKey
from typing import Optional
from machines import Machine
#from routines import Routine

class Part(Base):
    __tablename__="parts"
    p_id:Mapped[int]=mapped_column(primary_key=True)
    p_name:Mapped[str]=mapped_column(String(100),nullable=False)

    machine:Mapped["Machine"]= relationship("Machine", back_populates="parts")
    #routine:Mapped["Routine"]= relationship("Routine", back_populates="parts")