from sqlalchemy import text
from app.database import engine

def check_tables():
    print("\n----- Database Tables Check -----")
    try:
        with engine.connect() as connection:
            # Liste toutes les tables
            result = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            
            tables = result.fetchall()
            
            if not tables:
                print("❌ Aucune table trouvée dans la base de données")
            else:
                print("✅ Tables trouvées:")
                for table in tables:
                    print(f"\n• {table[0]}")
                    # Affiche la structure de chaque table
                    columns = connection.execute(text(f"""
                        SELECT column_name, data_type, character_maximum_length
                        FROM information_schema.columns
                        WHERE table_name = '{table[0]}'
                    """))
                    for col in columns:
                        print(f"  - {col[0]}: {col[1]}", end="")
                        if col[2]:
                            print(f" (max length: {col[2]})")
                        else:
                            print()

    except Exception as e:
        print(f"❌ Erreur lors de la vérification des tables: {str(e)}")

if __name__ == "__main__":
    check_tables() 