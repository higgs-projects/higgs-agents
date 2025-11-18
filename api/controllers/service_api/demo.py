from typing import Optional

from fastapi import APIRouter, HTTPException

from configs import higgs_config
from dependencies.services import HeroServiceDep, UserServiceDep
from models.hero import Hero
from models.user import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/demo", tags=["Demo"])


@router.get("/index")
async def index():
    return {
        "welcome": "Higgs Agents OpenAPI",
        "api_version": "v1",
        "server_version": higgs_config.CURRENT_VERSION,
    }


# Hero CRUD endpoints
@router.get("/heroes", response_model=list[Hero])
async def get_heroes(demo_service: HeroServiceDep, skip: int = 0, limit: int = 100):
    return demo_service.get_all_heroes(skip=skip, limit=limit)


@router.get("/heroes/{hero_id}", response_model=Hero)
async def get_hero(hero_id: int, demo_service: HeroServiceDep):
    hero = demo_service.get_hero_by_id(hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@router.post("/heroes", response_model=Hero)
async def create_hero(demo_service: HeroServiceDep, name: str, secret_name: str, age: Optional[int] = None):
    return demo_service.create_hero(name=name, secret_name=secret_name, age=age)


# User CRUD endpoints
@router.post("/users", response_model=UserRead)
async def create_user(user_service: UserServiceDep, user_data: UserCreate):
    try:
        return user_service.create_user(user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/users", response_model=list[UserRead])
async def get_users(user_service: UserServiceDep, skip: int = 0, limit: int = 100, active_only: bool = False):
    if active_only:
        return user_service.get_active_users()
    return user_service.get_all_users(skip=skip, limit=limit)


@router.get("/users/{user_id}", response_model=UserRead)
async def get_user(user_service: UserServiceDep, user_id: int):
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users/username/{username}", response_model=UserRead)
async def get_user_by_username(user_service: UserServiceDep, username: str):
    user = user_service.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=UserRead)
async def update_user(user_service: UserServiceDep, user_id: int, user_data: UserUpdate):
    try:
        user = user_service.update_user(user_id, user_data)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/users/{user_id}")
async def delete_user(user_service: UserServiceDep, user_id: int):
    if not user_service.delete_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}


@router.get("/users/search/{query}", response_model=list[UserRead])
async def search_users(user_service: UserServiceDep, query: str):
    return user_service.search_users(query)
