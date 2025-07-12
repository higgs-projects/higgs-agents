from sqlmodel import SQLModel

from models.engine import metadata


class Base(SQLModel):
    metadata = metadata
