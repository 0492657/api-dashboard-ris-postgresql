from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
from urllib.parse import quote_plus

db_user_ris = quote_plus(settings.db_username_ris)
db_password_ris = quote_plus(settings.db_password_ris)

db_user_orange = quote_plus(settings.db_username_orange)
db_pass_orange = quote_plus(settings.db_password_orange)

# Create an async database URL without the query parameters
ASYNC_DATABASE_URL_RIS = (
    f"postgresql+asyncpg://"
    f"{db_user_ris}:{db_password_ris}@"
    f"{settings.db_host_ris}:"
    f"{settings.db_port_ris}/"
    f"{settings.db_database_ris}"
)

ASYNC_DATABASE_URL_ORANGE =(
    f"postgresql+asyncpg://"
    f"{db_user_orange}:{db_pass_orange}@"
    f"{settings.db_host_orange}:"
    f"{settings.db_port_orange}/"
    f"{settings.db_database_orange}"
)

# Create an async SQLAlchemy engine with SSL configuration
engine = create_async_engine(
    ASYNC_DATABASE_URL_RIS, 
    echo=True,
    pool_pre_ping=True,
    pool_recycle=300
)

engine_orange = create_async_engine(
    ASYNC_DATABASE_URL_ORANGE,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=300
)

# Create a session factory for creating database sessions
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async_session_orange = sessionmaker(
    engine_orange,
    class_=AsyncSession,
    expire_on_commit=False
)

# Create a base class for declarative models
Base = declarative_base()

# Dependency to get an async database session
async def get_db():
    async with async_session() as session:
        try:
            yield session
            # await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def get_db_orange():
    async with async_session_orange() as session:
        try:
            yield session
            # await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()