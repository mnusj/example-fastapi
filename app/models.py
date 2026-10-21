from .database import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from sqlalchemy import func, ForeignKey, Column


class Post(Base):
  __tablename__ = "post"
  
  # typehints determines DB column types automatically
  id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
  title: Mapped[str] = mapped_column(nullable=False)
  content: Mapped[str] = mapped_column(nullable=False)
  
  # Default values and server defaults (postgres now() timestamp)
  published: Mapped[bool] = mapped_column(default=True, server_default="TRUE")
  created_at: Mapped[datetime] = mapped_column(server_default=func.now())
  owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False )
  
  
class User(Base):
  __tablename__ = "users"
  email: Mapped[str] = mapped_column(nullable=False, unique=True)
  password: Mapped[str] = mapped_column(nullable=False)
  id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
  created_at: Mapped[datetime] = mapped_column(server_default=func.now()) 
  
  
class Vote(Base):
  __tablename__ = "votes"
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
  post_id: Mapped[int] = mapped_column(ForeignKey("post.id", ondelete="CASCADE"), primary_key=True)