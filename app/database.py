from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

# URL de la base de données avec le préfixe async
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL.replace(
    "postgresql://", "postgresql+asyncpg://"
)

# Création du moteur asynchrone
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

# Session asynchrone
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

# Dépendance pour obtenir une session
async def get_db():
    async with async_session() as session:
        yield session 