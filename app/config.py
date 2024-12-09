from pydantic_settings import BaseSettings
from pydantic import ConfigDict
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
    API_V1_STR: str = "/api"
    
    # Database
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    
    @property
    def DATABASE_URL(self) -> str:        
        password = quote_plus(self.DB_PASSWORD)
        url = f"postgresql://{self.DB_USER}:{password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return url

    # Utiliser ConfigDict au lieu de Config
    model_config = ConfigDict(
        env_file=ENV_FILE,
        case_sensitive=True
    )

settings = Settings()
print("Settings initialized") 