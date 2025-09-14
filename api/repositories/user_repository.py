from typing import Optional

from sqlmodel import Session, select

from models.user import User

from .base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: Session):
        super().__init__(session, User)

    def get_by_username(self, username: str) -> Optional[User]:
        statement = select(User).where(User.username == username)
        return self.session.exec(statement).first()

    def get_by_email(self, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        return self.session.exec(statement).first()

    def get_active_users(self) -> list[User]:
        statement = select(User).where(User.is_active == True)
        return list(self.session.exec(statement).all())

    def search_by_name(self, name_query: str) -> list[User]:
        statement = select(User).where(
            User.full_name.contains(name_query) |
            User.username.contains(name_query)
        )
        return list(self.session.exec(statement).all())