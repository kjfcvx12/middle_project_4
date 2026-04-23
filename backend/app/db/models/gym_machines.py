from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .gyms import Gym
    from .machines import Machine


class Gym_Machine(Base):
    __tablename__ = "gym_machines"

    g_m_id: Mapped[int] = mapped_column(primary_key=True)

    g_id: Mapped[Optional[int]] = mapped_column(ForeignKey("gyms.g_id", ondelete="SET NULL"))
    m_id: Mapped[int] = mapped_column(ForeignKey("machines.m_id"))

    qty: Mapped[int] = mapped_column(nullable=False, default=1)

    gym: Mapped["Gym"]=relationship("Gym",back_populates="gym_machines")
    machine: Mapped["Machine"] = relationship("Machine", back_populates="gym_machines")