from sqlmodel import Field

from .base import Base


class Hero(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None
