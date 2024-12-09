### Endpoints

| Endpoint | Description | Payload & Réponse |
|----------|-------------|-------------------|
| **Configuration** |
| GET /api/v1/config/foods | Liste des aliments de référence | Query: `?language=fr` <br>Response: ```json [{ "id": "tomato", "name": "Tomate", "category": "VEGETABLES", "unit_type": "UNIT", "default_quantity": 1 }, ...] ``` |
| **Authentification** |
| POST /api/auth/register | Inscription d'un nouvel utilisateur | Request: ```json { "email": "user@example.com", "password": "secret", "name": "John Doe" }``` <br>Response: ```json { "token": "jwt_token", "user": { "id": 1, "email": "user@example.com", "name": "John Doe" } }``` |
| POST /api/auth/login | Connexion utilisateur | Request: ```json { "email": "user@example.com", "password": "secret" }``` <br>Response: ```json { "token": "jwt_token" }``` |
| POST /api/auth/logout | Déconnexion | Request: ∅ <br>Response: ```json { "message": "Déconnecté avec succès" }``` |
| **Événements** |
| GET /api/events | Liste des événements (paginée) | Response: ```json { "items": [...], "total": 100, "page": 1, "per_page": 20 }``` |
| POST /api/events | Création d'un événement | Request: ```json { "title": "Meeting", "start_time": "2024-03-21T14:00:00+01:00", "end_time": "2024-03-21T15:00:00+01:00", "timezone": "Europe/Paris" }``` <br>Response: ```json { "id": 1, "title": "Meeting", ... }``` |
| PUT /api/events/{id} | Modification d'un événement | Request: ```json { "title": "Updated Meeting" }``` <br>Response: ```json { "id": 1, "title": "Updated Meeting", ... }``` |
| DELETE /api/events/{id} | Suppression d'un événement | Response: ```json { "message": "Événement supprimé" }``` |
| POST /api/events/{id}/photos | Ajout d'une photo | Request: `multipart/form-data` avec fichier image <br>Response: ```json { "photo_url": "https://..." }``` |
| GET /api/events/search | Recherche d'événements | Query: `?q=meeting&start_date=2024-03-21` <br>Response: ```json { "items": [...], "total": 5 }``` |
| **Synchronisation** |
| GET /api/events/sync | Récupère les modifications depuis last_sync | Query: `?last_sync=2024-03-21T14:00:00Z` <br>Response: ```json { "created": [...], "updated": [...], "deleted": [...] }``` |
| POST /api/events/sync | Envoie les modifications locales | Request: ```json { "created": [...], "updated": [...], "deleted": [...] }``` |
| **Export** |
| GET /api/export/events/csv | Export CSV des événements | Response: `text/csv` fichier |
| GET /api/export/events/pdf | Export PDF des événements | Response: `application/pdf` fichier |
| **Configuration** |
| GET /api/config/timezones | Liste des fuseaux horaires | Response: ```json { "timezones": ["Europe/Paris", "America/New_York", ...] }``` |
| GET /api/config/app-version | Version minimale requise | Response: ```json { "min_version": "1.0.0", "latest_version": "1.2.0" }``` |
| **Notifications** |
| GET /api/notifications | Liste des notifications | Response: ```json { "items": [{ "id": 1, "message": "Nouveau commentaire", "read": false }] }``` |
| PUT /api/notifications/{id}/read | Marquer comme lu | Response: ```json { "id": 1, "read": true }``` |
| **Utilisateur** |
| GET /api/users/me | Profil utilisateur | Response: ```json { "id": 1, "email": "user@example.com", "preferences": {...} }``` |
| PUT /api/users/preferences | Mise à jour préférences | Request: ```json { "timezone": "Europe/Paris", "notification_enabled": true }``` |

### Notes sur l'API

- Tous les endpoints (sauf auth) nécessitent un header `Authorization: Bearer <token>`
- Les dates sont en ISO 8601 avec timezone
- La pagination utilise les paramètres `page` et `per_page`
- Les réponses d'erreur suivent le format : ```json { "error": "message", "code": "ERROR_CODE" }```
- Les listes paginées retournent toujours : ```json { "items": [...], "total": n, "page": x, "per_page": y }```
- Le paramètre `language` accepte les codes ISO 639-1 (ex: 'fr', 'en', 'de')
