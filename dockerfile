# Image de base Python
FROM python:3.9-slim

# Définition du répertoire de travail
WORKDIR /app

# Installation des dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copie des fichiers de dépendances
COPY requirements.txt .

# Installation des dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY . .

# Exposition du port
EXPOSE 9095

# Commande de démarrage avec uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9095"] 