from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from models.engine import get_session
from services.hero_service import HeroService
from services.user_service import UserService

# Module-level dependency annotations
SessionDep = Annotated[Session, Depends(get_session)]


def get_hero_service(session: SessionDep) -> HeroService:
    return HeroService(session)


def get_user_service(session: SessionDep) -> UserService:
    return UserService(session)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
HeroServiceDep = Annotated[HeroService, Depends(get_hero_service)]
