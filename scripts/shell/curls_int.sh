#!/bin/bash

# Configuration
API_URL="http://localhost:9095"
EMAIL="test@example.com"
PASSWORD="password123"

echo "🔵 1. Création de l'utilisateur"
echo "curl -X POST \"$API_URL/auth/register\" -H \"Content-Type: application/json\" -d '{\"email\": \"$EMAIL\", \"password\": \"$PASSWORD\"}'"
curl -X POST "$API_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$EMAIL\",
    \"password\": \"$PASSWORD\"
  }"
echo -e "\n"

echo "🔵 2. Login pour obtenir le token"
echo "curl -X POST \"$API_URL/auth/login\" -H \"Content-Type: application/x-www-form-urlencoded\" -d \"username=$EMAIL&password=$PASSWORD\""
TOKEN=$(curl -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=$EMAIL&password=$PASSWORD" | jq -r '.access_token')
echo "Token obtenu: $TOKEN"
echo -e "\n"

echo "🔵 3. Création d'un event avec meal_items"
echo "curl -X POST \"$API_URL/api/events\" -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" -d '{\"type\": \"MEAL\", \"date\": \"2024-03-15T12:30:00\", \"notes\": \"Déjeuner\", \"meal_items\": [{\"food_id\": 1, \"quantity\": 100.0}, {\"food_id\": 2, \"quantity\": 200.0}]}'"
curl -X POST "$API_URL/api/events" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "MEAL",
    "date": "2024-03-15T12:30:00",
    "notes": "Déjeuner",
    "meal_items": [
      {
        "food_id": 1,
        "quantity": 100.0
      },
      {
        "food_id": 2,
        "quantity": 200.0
      }
    ]
  }'
echo -e "\n"

echo "🔵 4. Récupération des events"
echo "curl -X GET \"$API_URL/api/events\" -H \"Authorization: Bearer $TOKEN\""
curl -X GET "$API_URL/api/events" \
  -H "Authorization: Bearer $TOKEN"
echo -e "\n"

echo "🔵 5. Récupération d'un event spécifique (id=1)"
echo "curl -X GET \"$API_URL/api/events/1\" -H \"Authorization: Bearer $TOKEN\""
curl -X GET "$API_URL/api/events/1" \
  -H "Authorization: Bearer $TOKEN"
echo -e "\n"

echo "🔵 6. Création d'un event avec un food_id invalide (pour tester la validation)"
echo "curl -X POST \"$API_URL/api/events\" -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" -d '{\"type\": \"MEAL\", \"date\": \"2024-03-15T12:30:00\", \"notes\": \"Déjeuner invalide\", \"meal_items\": [{\"food_id\": 999, \"quantity\": 100.0}]}'"
curl -X POST "$API_URL/api/events" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "MEAL",
    "date": "2024-03-15T12:30:00",
    "notes": "Déjeuner invalide",
    "meal_items": [
      {
        "food_id": 999,
        "quantity": 100.0
      }
    ]
  }'
echo -e "\n"

echo "🔵 7. Mise à jour d'un event existant"
echo "curl -X PUT \"$API_URL/api/events/1\" -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" -d '{\"notes\": \"Déjeuner modifié\", \"meal_items\": [{\"food_id\": 1, \"quantity\": 150.0}]}'"
curl -X PUT "$API_URL/api/events/1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "notes": "Déjeuner modifié",
    "meal_items": [
      {
        "food_id": 1,
        "quantity": 150.0
      }
    ]
  }'
echo -e "\n"

echo "🔵 8. Vérification finale des events"
echo "curl -X GET \"$API_URL/api/events\" -H \"Authorization: Bearer $TOKEN\""
curl -X GET "$API_URL/api/events" \
  -H "Authorization: Bearer $TOKEN"
echo -e "\n"
