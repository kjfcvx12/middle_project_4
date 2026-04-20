from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .users import User
    from .comments import Comment



class Like_Comment(Base):
    __tablename__ = "like_comments"

    l_c_id: Mapped[int] = mapped_column(primary_key=True)
    
    # 외래키 설정
    u_id: Mapped[int] = mapped_column(ForeignKey("users.u_id",ondelete="SET NULL"))
    c_id: Mapped[int] = mapped_column(ForeignKey("comments.cw_id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="like_comments")
    comment: Mapped["Comment"] = relationship(back_populates="like_comments")


