from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String
from typing import TYPE_CHECKING
from app.db.database import Base

if TYPE_CHECKING:
    from app.db.models.logs import Log

class Log_Detail(Base):
    __tablename__ = "log_details"

    log_d_id: Mapped[int] = mapped_column(primary_key=True)

    # cascade 추가
    log_id: Mapped[int] = mapped_column(
        ForeignKey("logs.log_id", ondelete="CASCADE")
    )

    sets: Mapped[int] = mapped_column(nullable=False)
    reps: Mapped[int] = mapped_column(nullable=False)

    fail_memo: Mapped[str | None] = mapped_column(String(100))
    memo: Mapped[str] = mapped_column(String(300), nullable=False)

    log: Mapped["Log"] = relationship(back_populates="details")