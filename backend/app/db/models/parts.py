from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .machines import Machine
    from .routines import Routine
    


class Part(Base):
    __tablename__="parts"
    p_id:Mapped[int]=mapped_column(primary_key=True)
    p_name:Mapped[str]=mapped_column(String(100),nullable=False)

    machines:Mapped[list["Machine"]]= relationship("Machine", back_populates="part")
    routines:Mapped[list["Routine"]]= relationship("Routine", back_populates="part")