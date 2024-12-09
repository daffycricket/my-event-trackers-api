from app.database import Base, engine
from app.models.event import Event  # Import existant
from app.models.food import Food    # Nouvel import
from sqlalchemy import text
from scripts.data.static_foods import STATIC_FOODS_FR, STATIC_FOODS_EN
import sys
from sqlalchemy.orm import sessionmaker

def drop_tables():
    print("\n----- Dropping all tables -----")
    try:
        Base.metadata.drop_all(bind=engine)
        print("✅ All tables dropped successfully")
    except Exception as e:
        print(f"❌ Error dropping tables: {str(e)}")
        sys.exit(1)

def load_static_data(session):
    print("\n----- Loading static data -----")
    try:
        # Charger les aliments
        for food_data in STATIC_FOODS_FR + STATIC_FOODS_EN:
            food = Food(**food_data)
            session.add(food)
        
        session.commit()
        print("✅ Static data loaded successfully")
    except Exception as e:
        session.rollback()
        print(f"❌ Error loading static data: {str(e)}")
        sys.exit(1)

def init_db(drop_first=False):
    print("\n----- Database Initialization -----")
    print(f"Using database URL: {engine.url}")
    
    try:
        # Vérifier la connexion
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Database connection successful")
        
        if drop_first:
            drop_tables()
        
        # Créer les tables
        print("\nCreating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created")
        
        # Vérifier les tables créées
        with engine.connect() as connection:
            result = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            tables = result.fetchall()
            print("\nTables in database:")
            for table in tables:
                print(f"• {table[0]}")
        
        # Créer une session pour charger les données
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Charger les données statiques
        load_static_data(session)
        
        session.close()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Si --drop est passé en argument, on drop d'abord
    drop_first = "--drop" in sys.argv
    init_db(drop_first) 