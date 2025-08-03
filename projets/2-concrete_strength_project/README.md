# Concrete Strength Predictor

Prédiction de la résistance (en compression simple) du béton à partir de sa composition et durée de cure, via une API FastAPI et un dashboard Streamlit.  
Le projet inclut aussi une base PostgreSQL pour le stockage du dataset d'entraînement du modèle Machine Learning.

---

## 🧱 Description

Ce projet propose une application complète pour :

- Ingestion, nettoyage et stockage des données béton dans une base PostgreSQL.
- Entraînement de différents modèles de machine learning et sauvegarde du meilleur (XGBoost) pour prédire la résistance à la compression du béton.
- API REST avec FastAPI pour exposer les prédictions individuelles et batch.
- Dashboard Streamlit offrant une interface utilisateur simple pour effectuer des prédictions.

---

## 🚀 Fonctionnalités

- Prédiction individuelle via formulaire web.
- Prédiction batch via import de fichier CSV.
- Stockage des données et modèles dans des dossiers dédiés.
- Conteneurisation via Docker avec orchestration Docker Compose.


---

## 🛠️ Prérequis

- Docker et Docker Compose installés  
- [Make](https://www.gnu.org/software/make/) (optionnel, pour simplifier certaines commandes)  
- Variables d'environnement définies dans un fichier `.env` (à adapter selon votre environnement) :

```env
POSTGRES_DB=concrete_db
POSTGRES_USER=concrete_user
POSTGRES_PASSWORD=your_password
API_URL=http://localhost:8000
