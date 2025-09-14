from abc import ABC
from typing import Generic, Optional, TypeVar

from sqlmodel import Session, select

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType], ABC):
    def __init__(self, session: Session, model_class: type[ModelType]):
        self.session = session
        self.model_class = model_class

    def create(self, obj: ModelType) -> ModelType:
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def get_by_id(self, id: int) -> Optional[ModelType]:
        return self.session.get(self.model_class, id)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ModelType]:
        statement = select(self.model_class).offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def update(self, obj: ModelType) -> ModelType:
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def delete(self, obj: ModelType) -> None:
        self.session.delete(obj)
        self.session.commit()

    def delete_by_id(self, id: int) -> bool:
        obj = self.get_by_id(id)
        if obj:
            self.delete(obj)
            return True
        return False