from datetime import datetime

from sqlmodel import Field

from .base import Base


class User(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    full_name: str | None = None
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserCreate(Base):
    username: str
    email: str
    full_name: str | None = None


class UserUpdate(Base):
    username: str | None = None
    email: str | None = None
    full_name: str | None = None
    is_active: bool | None = None


class UserRead(Base):
    id: int
    username: str
    email: str
    full_name: str | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime