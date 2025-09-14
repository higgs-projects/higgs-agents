from typing import Optional

from sqlmodel import Session, select

from models.hero import Hero

from .base import BaseRepository


class HeroRepository(BaseRepository[Hero]):
    def __init__(self, session: Session):
        super().__init__(session, Hero)

    def get_by_name(self, name: str) -> Optional[Hero]:
        statement = select(Hero).where(Hero.name == name)
        return self.session.exec(statement).first()

    def get_by_secret_name(self, secret_name: str) -> Optional[Hero]:
        statement = select(Hero).where(Hero.secret_name == secret_name)
        return self.session.exec(statement).first()

    def get_by_age_range(self, min_age: int, max_age: int) -> list[Hero]:
        statement = select(Hero).where(
            Hero.age >= min_age,
            Hero.age <= max_age
        )
        return list(self.session.exec(statement).all())