from typing import Optional
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from database import Base


class Users(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str] = mapped_column(nullable=False)
    ban: Mapped[bool] = mapped_column(default=False)

    url = relationship("URLS", back_populates="user", cascade="all, delete-orphan")


class URLS(Base):
    __tablename__ = 'urls'
    id: Mapped[str] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    url: Mapped[str] = mapped_column(index=True)
    click: Mapped[int] = mapped_column(default=0)

    user = relationship("Users", back_populates="url", foreign_keys=[user_id])
