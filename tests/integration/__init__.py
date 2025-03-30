from typing import Dict
import pytest
from fastapi import status

# URLs pour les tests d'intégration
BASE_URL = "http://localhost:9095"  # URL de l'API déployée
BASE_URLS = {
    "auth": f"{BASE_URL}/auth",
    "events": f"{BASE_URL}/api/events",
    "foods": f"{BASE_URL}/api/config/foods",
    "health": f"{BASE_URL}/health"
}

# Données de test communes
TEST_USER = {
    "email": "test@example.com",
    "password": "password123"
}

# Utilitaires pour les tests
def get_auth_headers(client) -> Dict[str, str]:
    """Utilitaire pour obtenir les headers d'authentification"""
    # Login pour obtenir le token
    response = client.post(
        f"{BASE_URLS['auth']}/login",
        data={"username": TEST_USER["email"], "password": TEST_USER["password"]}
    )
    assert response.status_code == status.HTTP_200_OK
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def create_test_user(client) -> Dict:
    """Utilitaire pour créer un utilisateur de test"""
    response = client.post(f"{BASE_URLS['auth']}/register", json=TEST_USER)
    assert response.status_code == status.HTTP_200_OK
    return response.json()
