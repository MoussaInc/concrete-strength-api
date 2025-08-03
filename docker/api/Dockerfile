# docker/api/Dockerfile

FROM python:3.11-slim

# Répertoire pour l'application FastAPI
WORKDIR /app
COPY . .
ENV PYTHONPATH=/app

# Copie des fichiers nécessaires
COPY src/api/ ./api/
COPY models/ ./models/
COPY config/config.yaml ./config/config.yaml
COPY docker/api/requirements.txt .

# Installation des dépendances
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Port de l'API FastAPI
EXPOSE 8000

# Lancer l'API
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
