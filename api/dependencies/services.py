from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from models.engine import get_session
from services.demo_service import DemoService
from services.user_service import UserService

# Module-level dependency annotations
SessionDep = Annotated[Session, Depends(get_session)]


def get_demo_service(session: SessionDep) -> DemoService:
    return DemoService(session)


def get_user_service(session: SessionDep) -> UserService:
    return UserService(session)