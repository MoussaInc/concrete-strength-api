# docker/api/Dockerfile

FROM python:3.11-slim

# Dossier pour ton app
WORKDIR /app

# Copie tout le repo dans le conteneur (Render clone à la racine du repo)
COPY . .

# Déclare le PYTHONPATH
ENV PYTHONPATH=/app

# Installe les dépendances
RUN pip install --upgrade pip && \
    pip install -r docker/api/requirements.txt

# Expose le port de FastAPI
EXPOSE 8000

# Commande de démarrage
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
