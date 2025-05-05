from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Прямое подключение (можно потом вынести в .env при желании)
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/smartbusket"

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

Base = declarative_base()

# Dependency для получения сессии (если будет использоваться внутри FastAPI тоже можно переиспользовать)
async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
