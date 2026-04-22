from datetime import datetime

from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Post(Base):
    __tablename__ = "posts"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(String(100), nullable=False)
    published: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default='True')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    # When `ForeignKey` is present, the type of the mapped column is derived from the datatype of referenced column
    # param `nullable` defaults to `True` for non-primary key columns, and `False` for primary key columns
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))  

    owner: Mapped["User"] = relationship("User", back_populates="posts")

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )

    posts: Mapped[list["Post"]] = relationship("Post", back_populates="owner")


class Vote(Base):
    __tablename__ = "votes"

    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)