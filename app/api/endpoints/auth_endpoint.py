from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/register")
async def register(email: str, password: str, name: str):
    return {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "user": {
            "id": 1,
            "email": email,
            "name": name
        }
    }

@router.post("/login")
async def login(email: str, password: str):
    return {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }

@router.post("/logout")
async def logout():
    return {"message": "Déconnecté avec succès"} 