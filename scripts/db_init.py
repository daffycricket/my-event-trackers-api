import asyncio
from app.database import Base, engine
from app.models.event import Event
from app.models.food import Food
from app.models.user import User
from sqlalchemy import text
from scripts.data.static_foods import STATIC_FOODS_FR, STATIC_FOODS_EN
import sys
from sqlalchemy.ext.asyncio import AsyncSession

async def init_db(drop_all: bool = False):
    print("\n----- Database Initialization -----")
    print(f"Using database URL: {str(engine.url).replace(engine.url.password or '', '***')}")
    
    try:
        # Test de connexion
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        print("✅ Database connection successful\n")
        
        if drop_all:
            print("----- Dropping all tables -----")
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
            print("✅ All tables dropped successfully\n")
        
        print("Creating database tables...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Database tables created\n")
        
        # Liste des tables
        async with engine.begin() as conn:
            result = await conn.execute(text(
                "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
            ))
            tables = result.scalars().all()
        
        print("Tables in database:")
        for table in tables:
            print(f"• {table}")
        
        # Insertion des données statiques
        print("\n----- Loading static data -----")
        async with AsyncSession(engine) as session:
            for food in STATIC_FOODS_FR + STATIC_FOODS_EN:
                session.add(Food(**food))
            await session.commit()
        print("✅ Static data loaded successfully")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    drop_all = "--drop" in sys.argv
    asyncio.run(init_db(drop_all)) 