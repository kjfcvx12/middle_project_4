from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .users import User
    from .boards import Board


class Like_Board(Base):
    __tablename__ = "like_boards"

    l_b_id: Mapped[int] = mapped_column(primary_key=True)
    
    # 외래키 설정
    u_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.u_id",ondelete="SET NULL")) 
    b_id: Mapped[int] = mapped_column(ForeignKey("boards.b_id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="like_boards")
    board: Mapped["Board"] = relationship(back_populates="like_boards")
