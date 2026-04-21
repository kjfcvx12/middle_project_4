from datetime import datetime
from sqlalchemy import String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base

class Comment(Base):
    __tablename__ = "comments"

    c_id: Mapped[int] = mapped_column(primary_key=True)
    
    # 외래키 설정
    # user model push 후 = mapped_column(ForeignKey("users.u_id")) 넣기
    # like model push 후 l_id: Mapped[int] = mapped_column(ForeignKey("likes.l_id"),nullable=True) 넣기
    b_id: Mapped[int] = mapped_column(ForeignKey("boards.b_id"))
    u_id: Mapped[int] 
    
    
    # 댓글 내용 및 시간 기록
    c_content: Mapped[str] = mapped_column(String(300), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, 
        server_default=func.now(), 
        onupdate=func.now()
    )