from datetime import datetime
from sqlalchemy import String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base

class Comment(Base):
    __tablename__ = "comments"
    # 기본키 설정
    c_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # 외래키 설정
    b_id: Mapped[int] = mapped_column(ForeignKey("boards.b_id"))
    u_id: Mapped[int] = mapped_column(ForeignKey("users.u_id"))

    # 댓글 내용 및 시간 기록
    content: Mapped[str] = mapped_column(String(300), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, 
        server_default=func.now(), 
        onupdate=func.now()
    )