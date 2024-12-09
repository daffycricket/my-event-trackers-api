from sqlalchemy import text
from app.database import engine

def test_connection():
    try:
        # Tente de créer une connexion et d'exécuter une requête simple
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Connexion à la base de données réussie!")
            
            # Affiche la version de PostgreSQL
            version = connection.execute(text("SELECT version()")).scalar()
            print(f"📊 Version PostgreSQL: {version}")
            
    except Exception as e:
        print("❌ Erreur de connexion à la base de données:")
        print(e)

if __name__ == "__main__":
    test_connection() 