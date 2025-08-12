# src/api/schemas.py

from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class PredictionInput(BaseModel):
    """
    Schéma d'entrée pour une prédiction unique.

    Attributs:
        features (Dict[str, float]): Dictionnaire des features nécessaires,
                                    incluant les features dérivées (water_cement_ratio, binder, fine_to_coarse_ratio).
    """
    features: Dict[str, float] = Field(..., description="Dictionnaire des features avec clés : \
                                       cement, slag, fly_ash, water, superplasticizer, coarse_aggregate, fine_aggregate, age, \
                                       water_cement_ratio, binder, fine_to_coarse_ratio")

class PredictionOutput(BaseModel):
    """
    Schéma de sortie pour une prédiction unique.

    Attributs:
        predicted_strength_MPa (float): Résultat de la prédiction.
        message (Optional[str]): Message optionnel expliquant la source ou une règle métier.
        source (Optional[str]): Source de la prédiction (model ou business_rule).
    """
    predicted_strength_MPa: float
    message: Optional[str]
    source: Optional[str]

class BatchPredictionOutput(BaseModel):
    """
    Schéma de sortie pour une prédiction batch.

    Attributs:
        predicted_strengths_MPa (List[float]): Liste des prédictions pour chaque entrée.
        messages (List[Optional[str]]): Liste des messages optionnels pour chaque prédiction.
        source (Optional[str]): Source globale de la prédiction batch.
    """
    predicted_strengths_MPa: List[float]
    messages: List[Optional[str]]
    source: Optional[str]
