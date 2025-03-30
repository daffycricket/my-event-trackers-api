# Tests des endpoints d'authentification

import pytest
from fastapi import status
import httpx
from tests.integration import BASE_URLS
import uuid

def get_test_user():
    return {
        "email": f"test_{uuid.uuid4()}@example.com",
        "password": "test123",
        "first_name": "Test",
        "last_name": "User"
    }

def test_register_user():
    with httpx.Client() as client:
        test_user = get_test_user()
        response = client.post(f"{BASE_URLS['auth']}/register", json=test_user)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "id" in data
        assert data["email"] == test_user["email"]

def test_register_duplicate_user():
    with httpx.Client() as client:
        test_user = get_test_user()
        # Premier enregistrement
        client.post(f"{BASE_URLS['auth']}/register", json=test_user)
        # Tentative de dupliquer
        response = client.post(f"{BASE_URLS['auth']}/register", json=test_user)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_login_success():
    with httpx.Client() as client:
        test_user = get_test_user()
        # Créer l'utilisateur
        client.post(f"{BASE_URLS['auth']}/register", json=test_user)
        # Tenter de se connecter
        response = client.post(
            f"{BASE_URLS['auth']}/login",
            data={
                "username": test_user["email"],
                "password": test_user["password"]
            }
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"

def test_login_invalid_credentials():
    with httpx.Client() as client:
        test_user = get_test_user()
        # Créer l'utilisateur
        client.post(f"{BASE_URLS['auth']}/register", json=test_user)
        # Tenter de se connecter avec un mauvais mot de passe
        response = client.post(
            f"{BASE_URLS['auth']}/login",
            data={
                "username": test_user["email"],
                "password": "wrong_password"
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
