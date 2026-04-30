from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .gyms import Gym
    from .machines import Machine


class Gym_Machine(Base):
    __tablename__ = "gym_machines"

    g_m_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    g_id: Mapped[int] = mapped_column(
        ForeignKey("gyms.g_id", ondelete="CASCADE"),
        nullable=False
    )

    m_id: Mapped[int] = mapped_column(
        ForeignKey("machines.m_id", ondelete="CASCADE"),
        nullable=False
    )

    qty: Mapped[int] = mapped_column(nullable=False, default=1)

    gym: Mapped["Gym"] = relationship("Gym", back_populates="gym_machines")
    machine: Mapped["Machine"] = relationship("Machine", back_populates="gym_machines")

    __table_args__ = (
        UniqueConstraint("g_id", "m_id", name="uq_gym_machine"),
    )