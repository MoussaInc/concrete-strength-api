from fastapi import FastAPI, File, HTTPException, UploadFile, Request
from fastapi.responses import JSONResponse
import pandas as pd
from typing import Optional, Tuple
import traceback

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


@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        tb = traceback.format_exc()
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "traceback": tb}
        )


def safe_divide(numerator: float, denominator: float, epsilon: float = 1e-8) -> float:
    return float(numerator) / (float(denominator) if denominator != 0 else epsilon)


def apply_business_rules_single(features: dict) -> Tuple[Optional[float], Optional[str]]:
    cement = float(features.get("cement", 0))
    slag = float(features.get("slag", 0))
    fly_ash = float(features.get("fly_ash", 0))
    water = float(features.get("water", 0))
    
    total_binder = cement + slag + fly_ash

    if total_binder == 0:
        return 0.0, "Résistance forcée à 0 MPa car aucun liant présent."
    if water == 0:
        return 0.0, "Résistance forcée à 0 MPa car eau = 0."

    return None, None


@app.get("/")
async def root():
    return {"message": "Concrete Strength Prediction API est en ligne."}


@app.post("/predict", response_model=PredictionOutput)
async def predict(input_data: PredictionInput):
    try:
        features = {k: float(v) for k, v in input_data.features.items()}

        cement = features["cement"]
        slag = features["slag"]
        fly_ash = features["fly_ash"]
        water = features["water"]
        coarse = features["coarse_aggregate"]
        fine = features["fine_aggregate"]

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

        df = pd.DataFrame([features], columns=ALL_FEATURES)
        prediction = model.predict(df)[0]
        prediction = max(float(prediction), 0.0)
        return {
            "predicted_strength_MPa": f"{round(prediction, 3)}",
            "message": None,
            "source": "model"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne: {e}")


@app.post("/predict-batch", response_model=BatchPredictionOutput)
async def predict_batch(file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        file.file.close()

        missing_cols = [col for col in BASE_FEATURES if col not in df.columns]
        if missing_cols:
            raise HTTPException(
                status_code=400,
                detail=f"Colonnes manquantes : {', '.join(missing_cols)}"
            )

        for col in BASE_FEATURES:
            df[col] = df[col].astype(float)

        df["water_cement_ratio"] = df.apply(
            lambda row: safe_divide(row["water"], row["cement"]), axis=1
        )
        df["binder"] = df["cement"] + df["slag"] + df["fly_ash"]
        df["fine_to_coarse_ratio"] = df.apply(
            lambda row: safe_divide(row["fine_aggregate"], row["coarse_aggregate"]), axis=1
        )

        preds_raw = model.predict(df[ALL_FEATURES])
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
            "source": "mixed"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne batch: {e}")
