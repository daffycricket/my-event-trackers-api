# My Event Tracker API

API REST FastAPI pour le backend de l'application My Event Tracker.

## Description

Cette API fournit les services backend nécessaires pour l'application My Event Tracker, permettant la gestion des événements personnels avec :
- Création, lecture, mise à jour et suppression d'événements
- Filtrage par type d'événement
- Filtrage par dates
- Pagination des résultats

## Technologies utilisées

- Python 3.8+
- FastAPI
- SQLAlchemy
- PostgreSQL
- Uvicorn
- Alembic (migrations)

## Installation

1. Prérequis

Assurez-vous d'avoir installé
- Python 3.8 ou supérieur
- PostgreSQL
- pip

2. Création d'un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
# ou
.\venv\Scripts\activate  # Windows
```

3. Installation des dépendances principales
```bash
pip install -r requirements.txt
```

4. Installation des dépendances de test
```bash
pip install -r requirements-test.txt
```

5. Configuration

```bash
# Créez un fichier .env à la racine du projet
cp .env.example .env
# Modifiez les variables d'environnement selon votre configuration
```

## Démarrage

```bash
# Mode développement
uvicorn app.main:app --reload --port 9095

# Mode production
uvicorn app.main:app --host 0.0.0.0 --port 9095
```

## Points d'entrée API

### Événements
- `GET /api/v1/events` - Récupérer les événements
  - Paramètres : skip, limit, type, from_date, to_date
- `POST /api/v1/events` - Créer un événement
- `GET /api/v1/events/{event_id}` - Récupérer un événement
- `PUT /api/v1/events/{event_id}` - Modifier un événement
- `DELETE /api/v1/events/{event_id}` - Supprimer un événement

## Structure du projet

```
app/
  ├── api/           # Routes API
  │   └── endpoints/ # Points d'entrée API
  ├── core/          # Configuration centrale
  ├── models/        # Modèles SQLAlchemy
  ├── schemas/       # Schémas Pydantic
  ├── database.py    # Configuration base de données
  └── main.py        # Point d'entrée
```

## Documentation API

La documentation interactive de l'API est disponible aux URLs suivants une fois le serveur lancé :
- Swagger UI : `http://localhost:9095/docs`
- ReDoc : `http://localhost:9095/redoc`

## Tests

```bash
# Lancer les tests
pytest tests/ -v

# Lancer les tests avec couverture
pytest --cov=app tests/

# Lancer les tests avec rapport de couverture détaillé
pytest --cov=app --cov-report=term-missing tests/
```

## Migrations de base de données

```bash
# Créer une nouvelle migration
alembic revision --autogenerate -m "description"

# Appliquer les migrations
alembic upgrade head
```

## Contribution

1. Fork le projet
2. Créez votre branche (`git checkout -b feature/amazing-feature`)
3. Committez vos changements (`git commit -m 'Add amazing feature'`)
4. Push vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrez une Pull Request

## Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE.md](LICENSE.md) pour plus de détails.

