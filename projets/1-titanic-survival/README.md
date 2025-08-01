# 🛳️ Titanic - Prédiction de survie

Ce projet vise à prédire la survie des passagers du Titanic à partir de données démographiques et socio-économiques.

## 🎯 Objectifs

- Nettoyage et préparation des données (`pandas`)
- Analyse exploratoire (graphiques, corrélations)
- Modélisation avec des classifieurs :
  - `LogisticRegression`
  - `RandomForestClassifier`
  - `XGBoostClassifier`
- Évaluation des performances et interprétation des résultats

## 📊 Données

Source : [Kaggle - Titanic Dataset](https://www.kaggle.com/competitions/titanic/data)

Les données sont placées dans le dossier `./data/`.

## 🧪 Résultats clés

- **Précision du meilleur modèle** : ~83%
- **Variables influentes** : `Sexe`, `Classe (Pclass)`, `SibSp` (présence de proches à bord). 
- Étonnamment, le prix du billet (`Fare`), souvent perçu comme indicateur de statut, n’est pas si influent ici (comme quoi, on peut payer cher… et couler quand même. 😬).
- Visualisations et graphiques disponibles dans le notebook

## 🚀 Lancer le projet

Dans un environnement avec les dépendances installées (`pip install -r requirements.txt` à la racine du dépôt) :

```bash
jupyter notebook titanic.ipynb
