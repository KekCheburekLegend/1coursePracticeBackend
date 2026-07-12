from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from database import Base


class Users(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]

    # urls = relationship("URLS", back_populates="user")


class URLS(Base):
    __tablename__ = 'urls'
    id: Mapped[str] = mapped_column(primary_key=True)
    url: Mapped[str]
    # user_id: Mapped[int] = mapped_column(ForeignKey(Users.id))
    # click: Mapped[int] = mapped_column(default=0)

    # user = relationship("Users", back_populates="urls")
