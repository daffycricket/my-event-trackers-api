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

### Option 1 : Installation locale

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

### Option 2 : Installation avec Docker

1. Prérequis
- Docker
- Docker Compose

2. Configuration
```bash
# Créez un fichier .env à la racine du projet
cp .env.example .env
# Modifiez les variables d'environnement selon votre configuration
```

3. Démarrage avec Docker
```bash
# Construire et démarrer les conteneurs
docker-compose up --build

# Démarrer en mode détaché (background)
docker-compose up --build -d

# Arrêter les conteneurs
docker-compose down

# Redémarrer l'API (en cas de changements)
docker-compose restart api
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
tests/              # Tests
.env                # Variables d'environnement (DB_URL, etc.)
.env.example        # Example de configuration
.dockerignore       # Fichiers ignorés par Docker
docker-compose.yml  # Configuration Docker Compose
Dockerfile         # Configuration de l'image Docker
requirements.txt   # Dépendances Python
```

## Documentation API

La documentation interactive de l'API est disponible aux URLs suivants une fois le serveur lancé :
- Swagger UI : `http://localhost:9095/docs`
- ReDoc : `http://localhost:9095/redoc`

## Tests

```bash
# Lancer les tests
PYTHONPATH=$PYTHONPATH:. pytest tests/ -v -s

# Lancer les tests avec couverture
PYTHONPATH=$PYTHONPATH:. pytest tests/ -v -s --cov=app tests/

# Lancer les tests avec rapport de couverture détaillé
PYTHONPATH=$PYTHONPATH:. pytest tests/ -v -s --cov=app --cov-report=term-missing tests/
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

## Docker

### Fichiers de configuration
- `Dockerfile` : Configuration de l'image Docker
- `docker-compose.yml` : Orchestration des services
- `.dockerignore` : Liste des fichiers à ne pas inclure dans l'image
- `.env` : Variables d'environnement (base de données, etc.)

### Commandes Docker utiles
```bash
# Construction et démarrage
docker-compose up --build        # Construire et démarrer les conteneurs
docker-compose up --build -d     # Idem, en mode détaché (background)

# Gestion des conteneurs
docker-compose down             # Arrêter et supprimer les conteneurs
docker-compose stop            # Arrêter les conteneurs sans les supprimer
docker-compose start           # Démarrer les conteneurs existants
docker-compose restart api     # Redémarrer uniquement le service API

# Logs et debug
docker-compose logs           # Voir tous les logs
docker-compose logs -f api    # Suivre les logs de l'API
docker-compose ps            # Voir l'état des conteneurs

# Accès au conteneur
docker-compose exec api bash  # Ouvrir un terminal dans le conteneur API

# Nettoyage
docker-compose down --volumes  # Supprimer les conteneurs et les volumes
docker system prune           # Nettoyer les ressources non utilisées
```

### Variables d'environnement (.env)
```bash
POSTGRES_USER=events_tracker_appuser
POSTGRES_PASSWORD=your_password
POSTGRES_DB=events_tracker_testsdb
POSTGRES_HOST=your_host
POSTGRES_PORT=25432
```

### Développement avec Docker
Le code est monté en volume dans le conteneur, permettant le rechargement automatique du code en développement.

**Note importante :** 
- Les changements de code simples sont automatiquement pris en compte
- Les changements structurels nécessitent un `docker-compose restart api`
- Les modifications de dépendances nécessitent un `docker-compose up --build`

## Scripts de test

### Script de test d'intégration

Le script `scripts/shell/curls_int.sh` permet de tester l'ensemble des endpoints de l'API en effectuant des appels séquentiels.

#### Utilisation

```bash
# Mode compact (affichage minimal)
./scripts/shell/curls_int.sh

# Mode détaillé (avec les commandes et leurs résultats)
./scripts/shell/curls_int.sh --verbose
```

#### Modes d'affichage

1. Mode compact (par défaut)
   - Affiche uniquement les statuts (🟢/🔴) et les titres des appels
   - Format très condensé pour une lecture rapide des résultats
   - Exemple :
     ```
     🟢 0. Récupération des foods
     🟢 1. Création de l'utilisateur
     🟢 2. Login pour obtenir le token
     ```

2. Mode verbose (avec `--verbose`)
   - Affiche les statuts et titres
   - Montre la commande curl exécutée
   - Affiche le résultat complet de la commande
   - Sépare chaque appel par une ligne vide
   - Utile pour le debugging et l'analyse détaillée

