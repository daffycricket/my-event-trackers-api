import pytest
from sqlalchemy import text
from app.database import engine
from app.config import settings

@pytest.mark.asyncio
async def test_connection():
    try:
        # Tente de créer une connexion et d'exécuter une requête simple
        async with engine.connect() as connection:
            result = await connection.execute(text("SELECT 1"))
            print("✅ Connexion à la base de données réussie!")
            
            # Affiche la version de PostgreSQL
            version_result = await connection.execute(text("SELECT version()"))
            version_text = version_result.scalar()  # Pas besoin d'await ici
            print(f"📊 Version PostgreSQL: {version_text}")
            
            # Affiche les informations de connexion (sans le mot de passe)
            print(f"🔌 Connexion à : {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
            print(f"👤 Utilisateur : {settings.DB_USER}")
            
    except Exception as e:
        print("❌ Erreur de connexion à la base de données:")
        print(f"Type d'erreur : {type(e).__name__}")
        print(f"Message d'erreur : {str(e)}")
        print("\nVérifiez que :")
        print("1. La base de données est en cours d'exécution")
        print("2. Les informations de connexion dans .env sont correctes")
        print("3. Le pare-feu autorise la connexion au port spécifié")
        print("4. L'utilisateur a les permissions nécessaires")
        raise  # Relève l'exception pour que pytest puisse la capturer

if __name__ == "__main__":
    pytest.main() 