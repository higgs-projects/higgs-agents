from datetime import datetime
from typing import Optional

from sqlmodel import Session

from models.user import User, UserCreate, UserRead, UserUpdate
from repositories.user_repository import UserRepository


class UserService:
    def __init__(self, session: Session):
        self.session = session
        self.user_repo = UserRepository(session)

    def create_user(self, user_data: UserCreate) -> UserRead:
        # 检查用户名和邮箱是否已存在
        if self.user_repo.get_by_username(user_data.username):
            raise ValueError(f"Username '{user_data.username}' already exists")

        if self.user_repo.get_by_email(user_data.email):
            raise ValueError(f"Email '{user_data.email}' already exists")

        # 创建新用户
        user = User(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
        )

        created_user = self.user_repo.create(user)
        return UserRead.model_validate(created_user)

    def get_user(self, user_id: int) -> Optional[UserRead]:
        user = self.user_repo.get_by_id(user_id)
        if user:
            return UserRead.model_validate(user)
        return None

    def get_user_by_username(self, username: str) -> Optional[UserRead]:
        user = self.user_repo.get_by_username(username)
        if user:
            return UserRead.model_validate(user)
        return None

    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[UserRead]:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return None

        # 更新字段
        if user_data.username is not None:
            # 检查用户名是否已被其他用户使用
            existing = self.user_repo.get_by_username(user_data.username)
            if existing and existing.id != user_id:
                raise ValueError(f"Username '{user_data.username}' already exists")
            user.username = user_data.username

        if user_data.email is not None:
            # 检查邮箱是否已被其他用户使用
            existing = self.user_repo.get_by_email(user_data.email)
            if existing and existing.id != user_id:
                raise ValueError(f"Email '{user_data.email}' already exists")
            user.email = user_data.email

        if user_data.full_name is not None:
            user.full_name = user_data.full_name

        if user_data.is_active is not None:
            user.is_active = user_data.is_active

        user.updated_at = datetime.utcnow()

        updated_user = self.user_repo.update(user)
        return UserRead.model_validate(updated_user)

    def delete_user(self, user_id: int) -> bool:
        return self.user_repo.delete_by_id(user_id)

    def get_all_users(self, skip: int = 0, limit: int = 100) -> list[UserRead]:
        users = self.user_repo.get_all(skip=skip, limit=limit)
        return [UserRead.model_validate(user) for user in users]

    def get_active_users(self) -> list[UserRead]:
        users = self.user_repo.get_active_users()
        return [UserRead.model_validate(user) for user in users]

    def search_users(self, query: str) -> list[UserRead]:
        users = self.user_repo.search_by_name(query)
        return [UserRead.model_validate(user) for user in users]