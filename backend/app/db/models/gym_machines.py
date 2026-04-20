from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base


class Gym_Machine(Base):
    __tablename__ = "gym_machines"

    g_m_id: Mapped[int] = mapped_column(primary_key=True)

    g_id: Mapped[int] = mapped_column(ForeignKey("gyms.g_id"))
    m_id: Mapped[int] = mapped_column(ForeignKey("machines.m_id"))

    qty: Mapped[int] = mapped_column(nullable=False, default=1)