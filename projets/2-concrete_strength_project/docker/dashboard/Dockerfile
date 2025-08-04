# docker/dashboard/Dockerfile

FROM python:3.11-slim

# Répertoire pour Streamlit
WORKDIR /app

# Copie tout le contenu du repo cloné
COPY . .

# Définir PYTHONPATH
ENV PYTHONPATH=/app

# Installer les dépendances
RUN pip install --upgrade pip && \
    pip install -r docker/dashboard/requirements.txt

# Port pour Streamlit
EXPOSE 8501

# Démarrage l'application Streamlit
CMD ["streamlit", "run", "src/dashboard/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
