# src/ml/predict.py

import os
import pandas as pd
import joblib
import argparse
from typing import Union

"""
Script de prédiction de la résistance du béton à l'aide d'un modèle ML entraîné.

Ce script prend en entrée un fichier CSV contenant les caractéristiques des mélanges de béton,
calcule les variables dérivées nécessaires, charge un modèle entraîné (sous forme de pipeline),
effectue les prédictions, puis sauvegarde les résultats dans un nouveau fichier CSV.

Exemple d'exécution :
    python src/ml/predict.py --input data/to_predict/batch1.csv
"""

# Constantes
MODEL_PATH = "models/best_model.joblib"
PREDICTION_PATH = "data/predictions/predicted_strength.csv"

def add_derived_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule les variables dérivées nécessaires à la prédiction :
        - water_cement_ratio
        - binder (liant total)
        - fine_to_coarse_ratio

    Args:
        df (pd.DataFrame): Données d'entrée avec les colonnes d'origine.

    Returns:
        pd.DataFrame: Données enrichies des variables dérivées.
    """

    df = df.copy()
    df["water_cement_ratio"] = df["water"] / df["cement"]
    df["binder"] = df["cement"] + df["slag"] + df["fly_ash"]
    df["fine_to_coarse_ratio"] = df["fine_aggregate"] / df["coarse_aggregate"]
    return df

def main(input_path: Union[str, os.PathLike]) -> None:
    """
    Charge les données, applique les transformations, effectue les prédictions,
    et sauvegarde les résultats dans un fichier CSV.

    Args:
        input_path (str or Path): Chemin vers le fichier CSV à prédire.
    """

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Fichier d'entrée non trouvé : {input_path}")

    print(f"Chargement des données depuis : {input_path}")
    df = pd.read_csv(input_path)
    df = add_derived_features(df)

    print(f"Chargement du modèle depuis : {MODEL_PATH}")
    pipeline = joblib.load(MODEL_PATH)

    print("Prédictions en cours...")
    predictions = pipeline.predict(df)
    df["predicted_strength"] = predictions

    os.makedirs(os.path.dirname(PREDICTION_PATH), exist_ok=True)
    df.to_csv(PREDICTION_PATH, index=False)
    print(f"Prédictions sauvegardées dans : {PREDICTION_PATH}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script de prédiction de résistance du béton à partir d'un fichier CSV.")
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Chemin vers le fichier CSV d'entrée contenant les caractéristiques du béton."
    )
    args = parser.parse_args()
    main(args.input)
