# Concrete Strength Predictor

Prédiction de la résistance (en compression simple) du béton à partir de sa composition et durée de cure, via l'API FastAPI et un dashboard bord Streamlit. 
Le projet inclut aussi une base PostgreSQL pour le stockage du dataset d'entrainement du modèle ML.

---

## 🧱 Description

Ce projet propose une application complète pour :

- Ingestion, nettoyage et stockage des données béton dans une base PostgreSQL.
- Entraînement de differents modèles de machine learning et sauvegarde du meilleur (XGBoost) pour prédire la résistance à la compression du béton.
- API REST avec FastAPI pour exposer les prédictions individuelles et batch.
- Dashboard Streamlit pour une interface utilisateur simple permettant d’effectuer des prédictions.

---

## 🚀 Fonctionnalités

- Prédiction individuelle via formulaire web.
- Prédiction batch via import de fichier CSV.
- Stockage des données et modèles dans des dossiers dédiés.
- Conteneurisation via Docker avec orchestration docker-compose.

---

## 📂 Structure du projet
.
├── data
│   ├── predictions
│   │   └── predicted_strength.csv
│   ├── processed
│   │   └── concrete_data_clean.csv
│   └── raw
│       ├── concrete_data.csv
│       └── concrete_data.xls
├── docker
│   ├── api
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   └── dashboard
│       ├── Dockerfile
│       └── requirements.txt
├── docker-compose.yml
├── LICENSE
├── models
│   ├── best_model.joblib
│   └── xgboost_model.joblib
├── notebooks
│   ├── 01_eda.ipynb
│   └── 02_modeling.ipynb
├── README.md
├── script
│   └── run_app.sh
└── src
    ├── api
    │   ├── main.py
    │   ├── model_loader.py
    │   ├── __pycache__
    │   └── schemas.py
    ├── dashboard
    │   ├── app.py
    │   ├── components.py
    │   ├── __pycache__
    │   └── static
    ├── etl
    │   ├── 1-download_data.py
    │   ├── 2-clean_data.py
    │   ├── 3-load_to_db.py
    │   └── __init__.py
    └── ml
        ├── 1-train_model.py
        ├── 2-predict.py
        ├── 3-evaluate_model.py
        └── __init__.py

---

## 🛠️ Prérequis

- Docker et Docker Compose installés
- [Make](https://www.gnu.org/software/make/) (optionnel, pour simplifier certaines commandes)
- Variables d'environnement dans un fichier `.env` 

---

## ⚙️ Configuration

Créez un fichier `.env` à la racine du projet avec le contenu suivant (à adapter) :
    POSTGRES_DB=concrete_db
    POSTGRES_USER=concrete_user
    POSTGRES_PASSWORD=your_password
    API_URL=http://localhost:8000

---

## 🚀 Démarrage local avec Docker

Pour lancer tous les services (PostgreSQL, API FastAPI, Dashboard Streamlit) depuis la racine du projet:

```bash
docker-compose docker compose up --build
