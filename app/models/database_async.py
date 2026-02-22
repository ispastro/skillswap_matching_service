from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.config import settings

# Convert postgres:// to postgresql+asyncpg://
async_database_url = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")

# Create async engine
async_engine = create_async_engine(async_database_url, echo=False)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency to get async database session
async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session
