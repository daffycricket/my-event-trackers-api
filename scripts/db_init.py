import asyncio
from sqlalchemy import text
from app.database import engine
from app.models.food import Food
from app.models.meal_item import MealItem
from scripts.data.static_foods import STATIC_FOODS

async def load_foods(conn):
    print("\n----- Loading foods data -----")
    try:
        # Insérer d'abord les aliments
        for food in STATIC_FOODS:
            result = await conn.execute(
                text("""
                    INSERT INTO foods (name, category, unit_type, default_quantity)
                    VALUES (:name, :category, :unit_type, :default_quantity)
                    RETURNING id
                """),
                {
                    "name": food["name"],
                    "category": food["category"],
                    "unit_type": food["unit_type"],
                    "default_quantity": food["default_quantity"]
                }
            )
            food_id = result.scalar()
            
            # Puis insérer les labels pour chaque langue
            for lang, label in food["labels"].items():
                await conn.execute(
                    text("""
                        INSERT INTO labels (entity_type, entity_id, language, value)
                        VALUES ('food', :entity_id, :language, :value)
                    """),
                    {
                        "entity_id": food_id,
                        "language": lang,
                        "value": label
                    }
                )
        print("✅ Foods and labels data loaded successfully")
    except Exception as e:
        print(f"❌ Error loading foods: {e}")
        raise

async def init_db(drop_all: bool = False):
    print("\n----- Database Initialization -----")
    print(f"Using database URL: {str(engine.url).replace(engine.url.password, '***')}")
    
    try:
        async with engine.begin() as conn:
            # Test de connexion
            await conn.execute(text("SELECT 1"))
            print("✅ Database connection successful\n")

            if drop_all:
                print("----- Dropping all tables -----")
                # Drop tables in order
                await conn.execute(text("DROP TABLE IF EXISTS meal_items CASCADE"))
                await conn.execute(text("DROP TABLE IF EXISTS events CASCADE"))
                await conn.execute(text("DROP TABLE IF EXISTS labels CASCADE"))
                await conn.execute(text("DROP TABLE IF EXISTS foods CASCADE"))
                await conn.execute(text("DROP TABLE IF EXISTS users CASCADE"))
                print("✅ All tables dropped successfully\n")

            # Création des tables
            print("----- Creating tables -----")
            from app.models.base import Base
            from app.models.user import User
            from app.models.event import Event
            from app.models.food import Food
            from app.models.meal_item import MealItem
            from app.models.label import Label
            
            await conn.run_sync(Base.metadata.create_all)
            print("✅ Tables created successfully")

            # Chargement des aliments
            await load_foods(conn)

    except Exception as e:
        print(f"❌ Error: {e}")
        raise

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--drop', action='store_true', help='Drop all tables before creating them')
    args = parser.parse_args()
    
    asyncio.run(init_db(args.drop)) 