from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, func
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .users import User

class Note(Base):
    __tablename__ = "notes"

    n_id: Mapped[int] = mapped_column(primary_key=True)
    
    send_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.u_id", ondelete="SET NULL"))
    rece_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.u_id", ondelete="SET NULL"))
    
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(String(200), nullable=False)
    
    n_date: Mapped[datetime] = mapped_column(server_default=func.now())
    
    send_del: Mapped[bool] = mapped_column(default=False)
    rece_del: Mapped[bool] = mapped_column(default=False)
    
    sender: Mapped["User"] = relationship("User", foreign_keys=[send_id], back_populates="sent_notes")
    receiver: Mapped["User"] = relationship("User", foreign_keys=[rece_id], back_populates="received_notes")
