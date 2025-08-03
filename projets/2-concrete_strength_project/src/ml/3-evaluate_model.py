# src/ml/3-evaluate_model.py

import argparse
import pandas as pd
import joblib
from sklearn.metrics import mean_absolute_error, mean_squared_error, root_mean_squared_error
import os
import sys

MODEL_PATH = "models/best_model.joblib"

def load_data(file_path):
    """
    Charge les données depuis un fichier CSV.

    Args:
        file_path (str): Chemin vers le fichier CSV.

    Returns:
        tuple: (X, y) où X est un DataFrame des features et y la série des cibles.

    Raises:
        ValueError: Si la colonne 'strength' n'est pas présente dans les données.
        FileNotFoundError: Si le fichier n'existe pas.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Fichier non trouvé : {file_path}")

    df = pd.read_csv(file_path)
    if "strength" not in df.columns:
        raise ValueError("Le fichier d'entrée doit contenir la colonne 'strength'.")

    X = df.drop(columns=["strength"])
    y = df["strength"]
    return X, y

def evaluate(model, X, y):
    """
    Évalue la performance du modèle sur les données fournies.

    Args:
        model: Modèle sklearn ou pipeline entraîné.
        X (DataFrame): Données d'entrée.
        y (Series): Valeurs cibles réelles.

    Returns:
        tuple: (rmse, mae) les erreurs de prédiction.
    """

    y_pred = model.predict(X)
    rmse = root_mean_squared_error(y, y_pred)
    mae = mean_absolute_error(y, y_pred)
    return rmse, mae

def main(input_path):
    print(f"Chargement du modèle depuis : {MODEL_PATH}")
    if not os.path.exists(MODEL_PATH):
        print(f"Erreur : modèle non trouvé à {MODEL_PATH}")
        sys.exit(1)
    model = joblib.load(MODEL_PATH)

    try:
        print(f"Chargement des données depuis : {input_path}")
        X, y = load_data(input_path)
    except (FileNotFoundError, ValueError) as e:
        print(f"Erreur lors du chargement des données : {e}")
        sys.exit(1)

    print("Évaluation en cours...")
    rmse, mae = evaluate(model, X, y)

    print("\nRésultats de l'évaluation :")
    print(f"RMSE : {rmse:.2f}")
    print(f"MAE  : {mae:.2f}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Évaluer un modèle de prédiction de résistance du béton.")
    parser.add_argument("--input", required=True, help="Chemin vers le fichier CSV contenant les données d'évaluation (avec la colonne 'strength').")
    args = parser.parse_args()

    main(args.input)
