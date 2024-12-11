#!/bin/bash

# Configuration
API_URL="http://localhost:9095"
EMAIL="test@example.com"
PASSWORD="password123"
VERBOSE=false

# Traitement des arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --verbose) VERBOSE=true ;;
        *) echo "Option inconnue: $1"; exit 1 ;;
    esac
    shift
done

# Couleurs
GREEN="\033[32m"
RED="\033[31m"
RESET="\033[0m"

# Fonction pour exécuter une commande et afficher le résultat avec la bonne couleur
execute_command() {
    local title="$1"
    local command="$2"
    
    if eval "$command" > /tmp/curl_output 2>&1; then
        echo -e "${GREEN}🟢${RESET} $title"
        if $VERBOSE; then
            echo -e "Commande à exécuter: $command"
            cat /tmp/curl_output
            echo -e ""
        fi
        return 0
    else
        echo -e "${RED}🔴${RESET} $title"
        if $VERBOSE; then
            echo -e "Commande à exécuter: $command"
            cat /tmp/curl_output
            echo -e ""
        fi
        return 1
    fi
}

# 0. Récupération des foods
execute_command "0. Récupération des foods" \
"curl -X GET \"$API_URL/config/foods?language=fr\""

$VERBOSE && echo -e ""

# 1. Création de l'utilisateur
execute_command "1. Création de l'utilisateur" \
"curl -X POST \"$API_URL/auth/register\" -H \"Content-Type: application/json\" -d '{\"email\": \"$EMAIL\", \"password\": \"$PASSWORD\"}'"

$VERBOSE && echo -e ""

# 2. Login pour obtenir le token
TOKEN=$(curl -s -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=$EMAIL&password=$PASSWORD" | jq -r '.access_token')

execute_command "2. Login pour obtenir le token" \
"echo \"Token obtenu: $TOKEN\""

$VERBOSE && echo -e ""

# 3. Création d'un event avec meal_items
execute_command "3. Création d'un event avec meal_items" \
"curl -X POST \"$API_URL/api/events\" -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" -d '{
    \"type\": \"MEAL\",
    \"date\": \"2024-03-15T12:30:00\",
    \"notes\": \"Déjeuner\",
    \"meal_items\": [{\"food_id\": 1, \"quantity\": 100.0}, {\"food_id\": 2, \"quantity\": 200.0}]
}'"

$VERBOSE && echo -e ""

# 4. Récupération des events
execute_command "4. Récupération des events" \
"curl -X GET \"$API_URL/api/events\" -H \"Authorization: Bearer $TOKEN\""

$VERBOSE && echo -e ""

# 5. Récupération d'un event spécifique
execute_command "5. Récupération d'un event spécifique (id=1)" \
"curl -X GET \"$API_URL/api/events/1\" -H \"Authorization: Bearer $TOKEN\""

$VERBOSE && echo -e ""

# 6. Test de validation avec un food_id invalide
execute_command "6. Création d'un event avec un food_id invalide" \
"curl -X POST \"$API_URL/api/events\" -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" -d '{
    \"type\": \"MEAL\",
    \"date\": \"2024-03-15T12:30:00\",
    \"notes\": \"Déjeuner invalide\",
    \"meal_items\": [{\"food_id\": 999, \"quantity\": 100.0}]
}'"

$VERBOSE && echo -e ""

# 7. Mise à jour d'un event
execute_command "7. Mise à jour d'un event existant" \
"curl -X PUT \"$API_URL/api/events/1\" -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" -d '{
    \"notes\": \"Déjeuner modifié\",
    \"meal_items\": [{\"food_id\": 1, \"quantity\": 150.0}]
}'"

$VERBOSE && echo -e ""

# 8. Vérification finale
execute_command "8. Vérification finale des events" \
"curl -X GET \"$API_URL/api/events\" -H \"Authorization: Bearer $TOKEN\""
