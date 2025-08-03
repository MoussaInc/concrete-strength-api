# src/api/model_loader.py

import joblib
import os

MODEL_PATH = os.path.join("models", "best_model.joblib")

def load_model():
    """
    Charge et retourne le modèle ML sauvegardé.

    Vérifie que le fichier du modèle existe à l'emplacement défini par MODEL_PATH.

    Returns:
        model: Objet modèle chargé via joblib.

    Raises:
        FileNotFoundError: Si le fichier du modèle n'est pas trouvé.
        Exception: Pour toute autre erreur de chargement.
    """

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Modèle introuvable à l’emplacement : {MODEL_PATH}")
    try:
        model = joblib.load(MODEL_PATH)
        return model
    except Exception as e:
        raise RuntimeError(f"Erreur lors du chargement du modèle : {e}")

