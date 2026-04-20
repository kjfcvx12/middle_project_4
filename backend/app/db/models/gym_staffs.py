from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base


class Gym_Staff(Base):
    __tablename__ = "gym_staffs"

    g_s_id: Mapped[int] = mapped_column(primary_key=True)

    g_id: Mapped[int] = mapped_column(ForeignKey("gyms.g_id"))
    u_id: Mapped[int] = mapped_column(ForeignKey("users.u_id"))