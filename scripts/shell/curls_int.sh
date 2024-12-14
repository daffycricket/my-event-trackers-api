#!/bin/bash

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
ORANGE='\033[0;33m'
NC='\033[0m' # No Color

# Vérifier si le mode verbose est activé
VERBOSE=false
if [[ "$1" == "--verbose" ]]; then
    VERBOSE=true
fi

# Fonction pour afficher le résultat avec la bonne couleur
handle_response() {
    local title=$1
    local response=$2
    local http_code=$3
    local command=$4
    
    # Choisir la couleur et le symbole en fonction du code HTTP
    if [[ $http_code -ge 200 ]] && [[ $http_code -lt 300 ]]; then
        color=$GREEN
        bullet="●"
    elif [[ $http_code -ge 400 ]] && [[ $http_code -lt 600 ]]; then
        color=$RED
        bullet="●"
    else
        color=$ORANGE
        bullet="●"
    fi
    
    echo -e "${color}${bullet}${NC} ${title} ${color}(HTTP ${http_code})${NC}"
    if [ "$VERBOSE" = true ]; then
        echo "Commande à exécuter: $command"
        echo "$response"
        echo ""
    fi
}

API_URL="http://localhost:9095"

# 0. Récupération des foods
command="curl -X GET \"$API_URL/api/config/foods?language=fr\""
response=$(curl -s -w "\n%{http_code}" "$API_URL/api/config/foods?language=fr")
http_code=$(echo "$response" | tail -n1)
content=$(echo "$response" | sed '$d')
handle_response "Récupération des foods" "$content" "$http_code" "$command"

# 1. Création de l'utilisateur
command="curl -X POST \"$API_URL/auth/register\" -H \"Content-Type: application/json\" -d '{\"email\": \"test@example.com\", \"password\": \"password123\"}'"
response=$(curl -s -w "\n%{http_code}" -X POST "$API_URL/auth/register" \
    -H "Content-Type: application/json" \
    -d '{"email": "test@example.com", "password": "password123"}')
http_code=$(echo "$response" | tail -n1)
content=$(echo "$response" | sed '$d')
handle_response "Création de l'utilisateur" "$content" "$http_code" "$command"

# 2. Login pour obtenir le token
response=$(curl -s -w "\n%{http_code}" -X POST "$API_URL/auth/login" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=test@example.com&password=password123")
http_code=$(echo "$response" | tail -n1)
content=$(echo "$response" | sed '$d')
TOKEN=$(echo "$content" | jq -r .access_token)
handle_response "Login pour obtenir le token" "Token obtenu: $TOKEN" "$http_code" "curl -X POST \"$API_URL/auth/login\" -d \"username=test@example.com&password=password123\""

# 3. Création d'un event avec meal_items
command="curl -X POST \"$API_URL/api/events\" -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" -d '{
    \"type\": \"MEAL\",
    \"date\": \"2024-03-15T12:30:00\",
    \"notes\": \"Déjeuner\",
    \"data\": {\"meal_type\": \"lunch\"},
    \"meal_items\": [{\"name\": \"apple\", \"quantity\": 100.0}, {\"name\": \"banana\", \"quantity\": 200.0}]
}'"
response=$(curl -s -w "\n%{http_code}" -X POST "$API_URL/api/events" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
    "type": "MEAL",
    "date": "2024-03-15T12:30:00",
    "notes": "Déjeuner",
    "data": {"meal_type": "lunch"},
    "meal_items": [{"name": "apple", "quantity": 100.0}, {"name": "banana", "quantity": 200.0}]
}')
http_code=$(echo "$response" | tail -n1)
content=$(echo "$response" | sed '$d')
handle_response "Création d'un event avec meal_items" "$content" "$http_code" "$command"

# 4. Récupération des events
command="curl -X GET \"$API_URL/api/events\" -H \"Authorization: Bearer $TOKEN\""
response=$(curl -s -w "\n%{http_code}" -X GET "$API_URL/api/events" \
    -H "Authorization: Bearer $TOKEN")
http_code=$(echo "$response" | tail -n1)
content=$(echo "$response" | sed '$d')
handle_response "Récupération des events" "$content" "$http_code" "$command"

# 5. Récupération d'un event spécifique
command="curl -X GET \"$API_URL/api/events/1\" -H \"Authorization: Bearer $TOKEN\""
response=$(curl -s -w "\n%{http_code}" -X GET "$API_URL/api/events/1" \
    -H "Authorization: Bearer $TOKEN")
http_code=$(echo "$response" | tail -n1)
content=$(echo "$response" | sed '$d')
handle_response "Récupération d'un event spécifique (id=1)" "$content" "$http_code" "$command"

# 6. Test de validation avec un food_id invalide
command="curl -X POST \"$API_URL/api/events\" -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" -d '{
    \"type\": \"MEAL\",
    \"date\": \"2024-03-15T12:30:00\",
    \"notes\": \"Déjeuner invalide\",
    \"data\": {\"meal_type\": \"lunch\"},
    \"meal_items\": [{\"name\": \"invalid_food\", \"quantity\": 100.0}]
}'"
response=$(curl -s -w "\n%{http_code}" -X POST "$API_URL/api/events" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
    "type": "MEAL",
    "date": "2024-03-15T12:30:00",
    "notes": "Déjeuner invalide",
    "data": {"meal_type": "lunch"},
    "meal_items": [{"name": "invalid_food", "quantity": 100.0}]
}')
http_code=$(echo "$response" | tail -n1)
content=$(echo "$response" | sed '$d')
handle_response "Création d'un event avec un food_id invalide" "$content" "$http_code" "$command"

# 7. Mise à jour d'un event
command="curl -X PUT \"$API_URL/api/events/1\" -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" -d '{
    \"notes\": \"Déjeuner modifié\",
    \"data\": {\"meal_type\": \"lunch\"},
    \"meal_items\": [{\"name\": \"apple\", \"quantity\": 150.0}]
}'"
response=$(curl -s -w "\n%{http_code}" -X PUT "$API_URL/api/events/1" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
    "notes": "Déjeuner modifié",
    "data": {"meal_type": "lunch"},
    "meal_items": [{"name": "apple", "quantity": 150.0}]
}')
http_code=$(echo "$response" | tail -n1)
content=$(echo "$response" | sed '$d')
handle_response "Mise à jour d'un event existant" "$content" "$http_code" "$command"

# 8. Vérification finale
command="curl -X GET \"$API_URL/api/events\" -H \"Authorization: Bearer $TOKEN\""
response=$(curl -s -w "\n%{http_code}" -X GET "$API_URL/api/events" \
    -H "Authorization: Bearer $TOKEN")
http_code=$(echo "$response" | tail -n1)
content=$(echo "$response" | sed '$d')
handle_response "Vérification finale des events" "$content" "$http_code" "$command"

# 9. Création d'un event de type workout
command="curl -X POST \"$API_URL/api/events\" -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" -d '{
    \"type\": \"WORKOUT\",
    \"date\": \"2024-03-15T18:00:00\",
    \"notes\": \"Entraînement de course\",
    \"data\": {
        \"duration\": 60,
        \"calories_burned\": 500,
        \"workout_type\": \"running\"
    }
}'"
response=$(curl -s -w "\n%{http_code}" -X POST "$API_URL/api/events" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
    "type": "WORKOUT",
    "date": "2024-03-15T18:00:00",
    "notes": "Entraînement de course",
    "data": {
        "duration": 60,
        "calories_burned": 500,
        "workout_type": "running"
    }
}')
http_code=$(echo "$response" | tail -n1)
content=$(echo "$response" | sed '$d')
handle_response "Création d'un event workout" "$content" "$http_code" "$command"

# 10. Création d'un event de type repas
command="curl -X POST \"$API_URL/api/events\" -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" -d '{
    \"type\": \"MEAL\",
    \"date\": \"2024-03-15T12:30:00\",
    \"notes\": \"Déjeuner\",
    \"data\": {
        \"meal_type\": \"lunch\"
    },
    \"meal_items\": [
        {\"name\": \"apple\", \"quantity\": 1.0},
        {\"name\": \"banana\", \"quantity\": 1.0}
    ]
}'"
response=$(curl -s -w "\n%{http_code}" -X POST "$API_URL/api/events" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
    "type": "MEAL",
    "date": "2024-03-15T12:30:00",
    "notes": "Déjeuner",
    "data": {
        "meal_type": "lunch"
    },
    "meal_items": [
        {"name": "apple", "quantity": 1.0},
        {"name": "banana", "quantity": 1.0}
    ]
}')
http_code=$(echo "$response" | tail -n1)
content=$(echo "$response" | sed '$d')
handle_response "Création d'un event repas" "$content" "$http_code" "$command"
