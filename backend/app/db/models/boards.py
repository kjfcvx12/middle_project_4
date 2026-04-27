from datetime import datetime
from sqlalchemy import String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .users import User
    from .comments import Comment
    from .like_boards import Like_Board
    

class Board(Base):
    __tablename__ = "boards"
    # 기본키 설정
    b_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # 외래키 설정
    u_id: Mapped[int] = mapped_column(ForeignKey("users.u_id"))
    
    
    # 게시글 내용 및 시간 기록
    b_content: Mapped[str] = mapped_column(String(300), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, 
        server_default=func.now(), 
        onupdate=func.now()
    )
    #cascade
    user: Mapped["User"] = relationship("User", back_populates="boards")
    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="board",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    like_boards: Mapped[list["Like_Board"]] = relationship("Like_Board", back_populates="board")
