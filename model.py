from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.orm import relationship
from database import Base


class Users(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]


class URLS(Base):
    __tablename__ = 'urls'
    id: Mapped[str] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(index=True)
