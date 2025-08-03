# src/api/main.py

from fastapi import FastAPI, File, HTTPException, UploadFile
import pandas as pd

from src.api.model_loader import load_model
from src.api.schemas import PredictionInput, PredictionOutput, BatchPredictionOutput

app = FastAPI(title="Concrete Strength Prediction API")

# Chargement du modéle au démarrage
model = load_model()

BASE_FEATURES = [
    "cement", "slag", "fly_ash", "water",
    "superplasticizer", "coarse_aggregate", "fine_aggregate", "age"
]

DERIVED_FEATURES = [
    "water_cement_ratio",
    "binder",
    "fine_to_coarse_ratio"
]

ALL_FEATURES = BASE_FEATURES + DERIVED_FEATURES

@app.get("/")
async def root():
    """
    Endpoint racine pour vérifier que l'API est en ligne.
    """

    return {"message": "Concrete Strength Prediction API est en ligne."}

@app.post("/predict", response_model=PredictionOutput)
async def predict(input_data: PredictionInput):
    """
    Prédiction unique à partir des features fournies.

    Args:
        input_data (PredictionInput): Données d'entrée validées par Pydantic.

    Returns:
        PredictionOutput: Résultat de la prédiction (résistance béton).
    """

    try:
        # Convertir les features dict en DataFrame ligne unique
        df = pd.DataFrame([input_data.features], columns=ALL_FEATURES)

        # Prédiction
        prediction = model.predict(df)[0]

        # Retour formatté, arrondi à 3 décimales
        return {"predicted_strength_MPa": f"{round(float(prediction), 3)}"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de la prédiction: {e}")

@app.post("/predict-batch", response_model=BatchPredictionOutput)
async def predict_batch(file: UploadFile = File(...)):
    """
    Prédiction batch à partir d'un fichier CSV uploadé.

    Args:
        file (UploadFile): Fichier CSV contenant les features de plusieurs échantillons.

    Returns:
        BatchPredictionOutput: Liste des prédictions.
    """

    try:
        # Lire le CSV uploadé en DataFrame
        df = pd.read_csv(file.file)

        # Vérifier la présence des colonnes de base nécessaires
        missing_cols = [col for col in BASE_FEATURES if col not in df.columns]
        if missing_cols:
            raise HTTPException(
                status_code=400,
                detail=f"Colonnes manquantes dans le fichier uploadé : {', '.join(missing_cols)}"
            )

        # Calculer les features dérivées
        df["water_cement_ratio"] = df["water"] / df["cement"]
        df["binder"] = df["cement"] + df["slag"] + df["fly_ash"]
        df["fine_to_coarse_ratio"] = df["fine_aggregate"] / df["coarse_aggregate"]

        # Réorganiser les colonnes dans l'ordre attendu par le modèle
        df_final = df[ALL_FEATURES]

        # Faire la prédiction batch
        predictions = model.predict(df_final)
        preds = [float(round(p, 3)) for p in predictions]

        return {"predicted_strengths_MPa": preds}

    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="Le fichier uploadé est vide ou invalide.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de la prédiction batch : {e}")
