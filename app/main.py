from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .api.endpoints import (
    events_endpoint,
    auth_endpoint,
    users_endpoint,
    config_endpoint,
    export_endpoint
)
from .database import engine, Base

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier les origines exactes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routers
app.include_router(
    events_endpoint.router,
    prefix="/api/events",
    tags=["events"]
)

app.include_router(
    auth_endpoint.router,
    prefix="/api/auth",
    tags=["auth"]
)

app.include_router(
    users_endpoint.router,
    prefix="/api/users",
    tags=["users"]
)

app.include_router(
    config_endpoint.router,
    prefix="/api/config",
    tags=["config"]
)

app.include_router(
    export_endpoint.router,
    prefix="/api/export",
    tags=["export"]
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to My Event Tracker API",
        "docs_url": "/docs",
        "openapi_url": f"{settings.API_V1_STR}/openapi.json"
    }

import uvicorn

if __name__ == "__main__":
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created!")
    uvicorn.run("app.main:app", host="0.0.0.0", port=9095, reload=True) 