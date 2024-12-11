from typing import Optional, Any
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.database import get_db

# Configuration du transport (Bearer token)
bearer_transport = BearerTransport(tokenUrl="auth/login")

# Clé secrète pour les JWT - À mettre dans les variables d'environnement en production
SECRET = "your-secret-key"

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

# Backend d'authentification
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

# User Manager pour la logique métier
class UserManager(BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    def parse_id(self, value: Any) -> int:
        return int(value)

# Fonction pour obtenir le UserManager
async def get_user_db(session: AsyncSession = Depends(get_db)):
    yield SQLAlchemyUserDatabase(session, User)

async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

# Instance principale de FastAPIUsers
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

# Utilitaires pour protéger les routes
current_active_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)