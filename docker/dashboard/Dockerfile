# docker/dashboard/Dockerfile

FROM python:3.11-slim

# Répertoire pour Streamlit
WORKDIR /app
COPY . .
ENV PYTHONPATH=/app

# Copie des fichiers utiles
COPY src/dashboard/ ./dashboard/
COPY models/ ./models/
COPY config/config.yaml ./config/config.yaml
COPY docker/dashboard/requirements.txt .

# Installation des dépendances
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Port du dashboard Streamlit
EXPOSE 8501

# Lancer l'application Streamlit
CMD ["streamlit", "run", "dashboard/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
