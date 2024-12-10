from fastapi import APIRouter, Depends
from app.auth.config import auth_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead

router = APIRouter()

# Routes d'authentification
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)

# Route d'enregistrement
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

# Route utilisateur courant
router.include_router(
    fastapi_users.get_users_router(UserRead, UserRead),
    prefix="/users",
    tags=["users"],
) 