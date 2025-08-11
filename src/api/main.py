from fastapi import FastAPI, File, HTTPException, UploadFile
import pandas as pd
from typing import Optional, Tuple

from src.api.model_loader import load_model
from src.api.schemas import PredictionInput, PredictionOutput, BatchPredictionOutput

app = FastAPI(title="Concrete Strength Prediction API")

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

def safe_divide(numerator: float, denominator: float, epsilon: float = 1e-8) -> float:
    return float(numerator) / (float(denominator) if denominator != 0 else epsilon)

def apply_business_rules_single(features: dict) -> Tuple[Optional[float], Optional[str]]:
    """
    Applique les règles métier sur les features données.

    Returns:
        prediction_override (Optional[float]): valeur forcée si règle appliquée, sinon None.
        message (Optional[str]): message explicatif associé.
    """
    cement = float(features.get("cement", 0))
    slag = float(features.get("slag", 0))
    fly_ash = float(features.get("fly_ash", 0))
    water = float(features.get("water", 0))
    
    total_binder = cement + slag + fly_ash

    if total_binder == 0:
        return 0.0, "Résistance forcée à 0 MPa car aucun liant présent (cement, slag, fly_ash à 0)."

    if water == 0:
        return 0.0, "Résistance forcée à 0 MPa car eau (water) = 0, non-physique."

    return None, None

@app.get("/")
async def root():
    return {"message": "Concrete Strength Prediction API est en ligne."}

@app.post("/predict", response_model=PredictionOutput)
async def predict(input_data: PredictionInput):
    features = input_data.features.copy()

    cement = float(features.get("cement", 0))
    slag = float(features.get("slag", 0))
    fly_ash = float(features.get("fly_ash", 0))
    water = float(features.get("water", 0))
    coarse = float(features.get("coarse_aggregate", 0))
    fine = float(features.get("fine_aggregate", 0))

    features["water_cement_ratio"] = safe_divide(water, cement)
    features["binder"] = cement + slag + fly_ash
    features["fine_to_coarse_ratio"] = safe_divide(fine, coarse)

    prediction_override, message = apply_business_rules_single(features)
    if prediction_override is not None:
        return {
            "predicted_strength_MPa": f"{round(prediction_override, 3)}",
            "message": message,
            "source": "business_rule"
        }

    try:
        df = pd.DataFrame([features], columns=ALL_FEATURES)
        prediction = model.predict(df)[0]
        prediction = max(float(prediction), 0.0)
        return {
            "predicted_strength_MPa": f"{round(prediction, 3)}",
            "message": None,
            "source": "model"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de la prédiction: {e}")

@app.post("/predict-batch", response_model=BatchPredictionOutput)
async def predict_batch(file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        file.file.close() 

        missing_cols = [col for col in BASE_FEATURES if col not in df.columns]
        if missing_cols:
            raise HTTPException(
                status_code=400,
                detail=f"Colonnes manquantes dans le fichier uploadé : {', '.join(missing_cols)}"
            )

        df["water_cement_ratio"] = df.apply(
            lambda row: safe_divide(row["water"], row["cement"]), axis=1
        )
        df["binder"] = df["cement"] + df["slag"] + df["fly_ash"]
        df["fine_to_coarse_ratio"] = df.apply(
            lambda row: safe_divide(row["fine_aggregate"], row["coarse_aggregate"]), axis=1
        )

        df_final = df[ALL_FEATURES]
        preds_raw = model.predict(df_final)
        preds_clamped = []
        messages = []

        for idx, row in df.iterrows():
            features = row.to_dict()
            pred_override, msg = apply_business_rules_single(features)
            if pred_override is not None:
                preds_clamped.append(round(pred_override, 3))
                messages.append(msg)
            else:
                pred = max(float(preds_raw[idx]), 0.0)
                preds_clamped.append(round(pred, 3))
                messages.append(None)

        return {
            "predicted_strengths_MPa": preds_clamped,
            "messages": messages,
            "source": "mixed (business_rule + model)"
        }
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="Le fichier uploadé est vide ou invalide.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de la prédiction batch : {e}")
