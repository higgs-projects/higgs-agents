from typing import Optional

from sqlmodel import Session

from models.hero import Hero
from repositories.hero_repository import HeroRepository


class HeroService:
    def __init__(self, session: Session):
        self.session = session
        self.hero_repo = HeroRepository(session)

    def get_hero_by_id(self, hero_id: int) -> Optional[Hero]:
        return self.hero_repo.get_by_id(hero_id)

    def get_all_heroes(self, skip: int = 0, limit: int = 100) -> list[Hero]:
        return self.hero_repo.get_all(skip=skip, limit=limit)

    def create_hero(self, name: str, secret_name: str, age: Optional[int] = None) -> Hero:
        hero = Hero(name=name, secret_name=secret_name, age=age)
        return self.hero_repo.create(hero)
