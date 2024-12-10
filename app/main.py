from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth.config import auth_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead, UserUpdate
from .api.endpoints import (
    events_endpoint,
    config_endpoint
)

app = FastAPI()

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes d'authentification
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)

# Route d'enregistrement
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

# Routes de l'API
app.include_router(events_endpoint.router)
app.include_router(config_endpoint.router)