from pydantic_settings import BaseSettings
from typing import Optional
import os
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Obtenir le chemin absolu vers le fichier .env
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = os.path.join(BASE_DIR, '.env')

print(f"Looking for .env file at: {ENV_FILE}")
print(f"File exists: {os.path.exists(ENV_FILE)}")

# Charger le .env dans os.environ
load_dotenv(ENV_FILE, override=True)  # override=True force l'écrasement des variables existantes

class Settings(BaseSettings):
    # Base
    PROJECT_NAME: str = "My Event Tracker API"
    API_V1_STR: str = "/api/v1"
    
    # Database
    POSTGRES_USER: str = "default_user"
    POSTGRES_PASSWORD: str = "default_password"
    POSTGRES_DB: str = "default_db"
    POSTGRES_HOST: str = "default_host"
    POSTGRES_PORT: str = "5432"
    
    @property
    def DATABASE_URL(self) -> str:        
        password = quote_plus(self.POSTGRES_PASSWORD)
        url = f"postgresql://{self.POSTGRES_USER}:{password}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        return url

    class Config:
        env_file = ENV_FILE

settings = Settings()
print("Settings initialized") 