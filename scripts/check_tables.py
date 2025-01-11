import asyncio
from sqlalchemy import text
from app.database import engine

async def check_tables():
    print("\n----- Database Tables Check -----")
    try:
        async with engine.connect() as connection:
            # Liste toutes les tables
            result = await connection.execute(text("""
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
                    columns = await connection.execute(text(f"""
                        SELECT 
                            c.column_name,
                            c.data_type,
                            c.character_maximum_length,
                            c.column_default,
                            c.is_nullable,
                            string_agg(DISTINCT tc.constraint_type || ': ' || kcu.constraint_name, ', ') as constraints
                        FROM 
                            information_schema.columns c
                            LEFT JOIN information_schema.key_column_usage kcu 
                                ON c.table_name = kcu.table_name 
                                AND c.column_name = kcu.column_name
                            LEFT JOIN information_schema.table_constraints tc 
                                ON kcu.constraint_name = tc.constraint_name 
                                AND kcu.table_name = tc.table_name
                        WHERE c.table_name = '{table[0]}'
                        GROUP BY 
                            c.column_name,
                            c.data_type,
                            c.character_maximum_length,
                            c.column_default,
                            c.is_nullable
                        ORDER BY c.column_name
                    """))
                    
                    for col in columns:
                        info = [f"  - {col[0]}:"]
                        info.append(f"Type={col[1]}")
                        if col[2]:  # max length
                            info.append(f"MaxLen={col[2]}")
                        if col[3]:  # default
                            info.append(f"Default={col[3]}")
                        info.append(f"Nullable={'YES' if col[4] == 'YES' else 'NO'}")
                        if col[5]:  # constraints
                            info.append(f"Constraints=[{col[5]}]")
                        print(" ".join(info))

    except Exception as e:
        print(f"❌ Erreur lors de la vérification des tables: {str(e)}")

if __name__ == "__main__":
    asyncio.run(check_tables()) 