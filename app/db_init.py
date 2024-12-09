from app.database import engine, Base
from sqlalchemy import text
from app.config import settings

def init_db():
    print("\n----- Database Configuration -----")
    print(f"Connection URL: {settings.DATABASE_URL}")
    print(f"Engine URL: {engine.url}")

    print("\n----- Testing Connection -----")
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✓ Connection test successful")
    except Exception as e:
        print(f"✗ Connection failed: {str(e)}")
        return

    print("\n----- Dropping all tables -----")
    Base.metadata.drop_all(bind=engine)
    print("✓ Tables dropped")

    print("\n----- Creating tables -----")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created")

    # Lister les tables créées
    with engine.connect() as connection:
        result = connection.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """))
        tables = [row[0] for row in result]
        print("\nCreated tables:")
        for table in tables:
            print(f"\n• {table}")
            columns = connection.execute(text(f"""
                SELECT column_name, data_type, character_maximum_length
                FROM information_schema.columns
                WHERE table_name = '{table}'
            """))
            for col in columns:
                print(f"  - {col[0]}: {col[1]}", end="")
                if col[2]:
                    print(f" (max length: {col[2]})")
                else:
                    print()

if __name__ == "__main__":
    init_db()
    print("\n✓ Database initialization completed!") 