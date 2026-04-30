from datetime import datetime
from sqlalchemy import String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .boards import Board
    from .users import User
    from .like_comments import Like_Comment
    



class Comment(Base):
    __tablename__ = "comments"

    c_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # 외래키 설정
    # like model push 후 l_id: Mapped[int] = mapped_column(ForeignKey("likes.l_id"),nullable=True) 넣기
    b_id: Mapped[int] = mapped_column(ForeignKey("boards.b_id", ondelete="CASCADE"),nullable=False)
    u_id: Mapped[int] = mapped_column(ForeignKey("users.u_id"))
    
    
    # 댓글 내용 및 시간 기록
    c_content: Mapped[str] = mapped_column(String(300), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, 
        server_default=func.now(), 
        onupdate=func.now()
    )

    #cascade
    board: Mapped["Board"] = relationship(
        "Board",
        back_populates="comments"
    )

    user: Mapped["User"] = relationship("User", back_populates="comments")
    like_comments: Mapped[list["Like_Comment"]] = relationship("Like_Comment", back_populates="comment")