# src/api/schemas.py

from pydantic import BaseModel, conlist
from typing import List

class PredictionInput(BaseModel):
    """
    Schéma d'entrée pour une prédiction unique.

    Attributs:
        features (List[float]): Liste de 11 valeurs numériques correspondant aux features nécessaires,
                                incluant les features dérivées (water_cement_ratio, binder, fine_to_coarse_ratio).
    """
    features: conlist(float, min_length=11, max_length=11)  # type: ignore

class PredictionOutput(BaseModel):
    """
    Schéma de sortie pour une prédiction unique.

    Attributs:
        predicted_strength_MPa (str): Résultat de la prédiction sous forme de chaîne formatée.
    """

    predicted_strength_MPa: str

class BatchPredictionOutput(BaseModel):
    """
    Schéma de sortie pour une prédiction batch.

    Attributs:
        predicted_strengths_MPa (List[float]): Liste des prédictions pour chaque entrée.
    """
    
    predicted_strengths_MPa: List[float]
