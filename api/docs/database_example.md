# SQLModel 数据库读写示例

## 项目结构

基于SQLModel的数据库操作示例已经集成到现有项目中，采用了分层架构：

```
api/
├── models/                    # 数据模型层
│   ├── base.py               # 基础模型类
│   ├── hero.py               # Hero模型 (原有)
│   ├── user.py               # User模型 (新增)
│   └── engine.py             # 数据库引擎配置
├── repositories/             # 数据访问层 (新增)
│   ├── base.py               # 基础Repository类
│   ├── hero_repository.py    # Hero数据访问
│   └── user_repository.py    # User数据访问
├── services/                 # 业务逻辑层
│   ├── demo_service.py       # Demo业务服务 (扩展)
│   └── user_service.py       # User业务服务 (新增)
├── controllers/service_api/  # API控制器层
│   └── demo.py               # API端点 (扩展)
└── migrations/               # 数据库迁移
    └── versions/
        └── a1b2c3d4e5f6_add_user_table.py  # User表迁移
```

## 核心组件说明

### 1. 数据模型层 (Models)

#### Base模型
```python
# models/base.py
from sqlmodel import SQLModel

class Base(SQLModel):
    metadata = metadata
```

#### User模型
```python
# models/user.py
class User(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    full_name: str | None = None
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Pydantic模型用于API
class UserCreate(Base): ...
class UserUpdate(Base): ...
class UserRead(Base): ...
```

### 2. 数据访问层 (Repositories)

#### 基础Repository
```python
# repositories/base.py
class BaseRepository(Generic[ModelType], ABC):
    def create(self, obj: ModelType) -> ModelType: ...
    def get_by_id(self, id: int) -> Optional[ModelType]: ...
    def get_all(self, skip: int = 0, limit: int = 100) -> list[ModelType]: ...
    def update(self, obj: ModelType) -> ModelType: ...
    def delete(self, obj: ModelType) -> None: ...
    def delete_by_id(self, id: int) -> bool: ...
```

#### User Repository
```python
# repositories/user_repository.py
class UserRepository(BaseRepository[User]):
    def get_by_username(self, username: str) -> Optional[User]: ...
    def get_by_email(self, email: str) -> Optional[User]: ...
    def get_active_users(self) -> list[User]: ...
    def search_by_name(self, name_query: str) -> list[User]: ...
```

### 3. 业务逻辑层 (Services)

```python
# services/user_service.py
class UserService:
    def __init__(self, session: Session):
        self.session = session
        self.user_repo = UserRepository(session)

    def create_user(self, user_data: UserCreate) -> UserRead: ...
    def get_user(self, user_id: int) -> Optional[UserRead]: ...
    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[UserRead]: ...
    def delete_user(self, user_id: int) -> bool: ...
    # ... 更多业务方法
```

### 4. API控制器层 (Controllers)

```python
# controllers/service_api/demo.py

# 依赖注入
def get_user_service(session: Session = Depends(get_session)) -> UserService:
    return UserService(session)

# CRUD API端点
@router.post("/users", response_model=UserRead)
async def create_user(user_data: UserCreate, user_service: UserService = Depends(get_user_service)): ...

@router.get("/users/{user_id}", response_model=UserRead)
async def get_user(user_id: int, user_service: UserService = Depends(get_user_service)): ...

@router.put("/users/{user_id}", response_model=UserRead)
async def update_user(user_id: int, user_data: UserUpdate, user_service: UserService = Depends(get_user_service)): ...

@router.delete("/users/{user_id}")
async def delete_user(user_id: int, user_service: UserService = Depends(get_user_service)): ...
```

## API端点

所有端点都在 `/demo` 前缀下：

### Hero相关 (原有扩展)
- `GET /demo/heroes` - 获取所有Hero
- `GET /demo/heroes/{hero_id}` - 获取指定Hero
- `POST /demo/heroes` - 创建Hero

### User相关 (新增)
- `POST /demo/users` - 创建用户
- `GET /demo/users` - 获取用户列表 (支持分页和仅活跃用户过滤)
- `GET /demo/users/{user_id}` - 获取指定用户
- `GET /demo/users/username/{username}` - 根据用户名获取用户
- `PUT /demo/users/{user_id}` - 更新用户
- `DELETE /demo/users/{user_id}` - 删除用户
- `GET /demo/users/search/{query}` - 搜索用户

## 使用示例

### 创建用户
```bash
curl -X POST "http://localhost:8000/demo/users" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "full_name": "John Doe"
  }'
```

### 获取用户
```bash
curl "http://localhost:8000/demo/users/1"
```

### 更新用户
```bash
curl -X PUT "http://localhost:8000/demo/users/1" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Smith",
    "is_active": true
  }'
```

## 数据库迁移

运行迁移来创建User表：

```bash
# 应用迁移
uv run alembic -c ./migrations/alembic.ini upgrade head

# 查看迁移状态
uv run alembic -c ./migrations/alembic.ini current

# 回滚迁移
uv run alembic -c ./migrations/alembic.ini downgrade -1
```

## 架构优势

1. **分层清晰**: Models -> Repositories -> Services -> Controllers
2. **职责分离**: 每层都有明确的职责
3. **类型安全**: 基于SQLModel和Pydantic提供完整类型支持
4. **可测试性**: 依赖注入使得各层易于测试
5. **可扩展性**: 基于泛型的BaseRepository便于扩展新模型
6. **业务逻辑封装**: Service层封装复杂的业务逻辑和验证

## 扩展指南

要添加新的数据模型，按以下步骤：

1. 在 `models/` 中创建新模型文件
2. 在 `repositories/` 中继承BaseRepository创建数据访问类
3. 在 `services/` 中创建业务服务类
4. 在 `controllers/service_api/demo.py` 中添加API端点
5. 创建数据库迁移文件
6. 更新 `models/__init__.py` 导出新模型