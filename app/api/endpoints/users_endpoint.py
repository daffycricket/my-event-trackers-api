from fastapi import APIRouter

router = APIRouter()

@router.get("/me")
async def get_profile():
    return {
        "id": 1,
        "email": "user@example.com",
        "preferences": {
            "timezone": "Europe/Paris",
            "notification_enabled": True
        }
    }

@router.put("/preferences")
async def update_preferences(preferences: dict):
    return {
        "timezone": preferences.get("timezone"),
        "notification_enabled": preferences.get("notification_enabled")
    } 