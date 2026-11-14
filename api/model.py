"""Raccord entre l'API et le modèle entraîné au TP2.

L'API n'entraîne rien et ne connaît pas scikit-learn : elle appelle la fonction
predict() de src/predict.py, qui charge models/sentiment.joblib une seule fois.
"""
import sys
from pathlib import Path
from typing import Final, TypedDict

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE / "src"))
from api.schemas import Etiquette  # noqa: E402
from predict import MODELE, charger_modele  # noqa: E402  (fonctions du TP2)
from predict import predict as _predict  # noqa: E402

__all__ = ["MODELE", "SEUIL_ABSTENTION", "Prediction", "SentimentClassifier", "load_model"]

# Sous ce seuil de confiance, le modèle s'abstient : un humain tranche (courbe : src/courbe_seuil.py).
SEUIL_ABSTENTION: Final = 0.60

# Étiquettes du modèle (TP2, minuscules) -> étiquettes du contrat de l'API.
CORRESPONDANCE: Final[dict[str, Etiquette]] = {"positive": "POSITIVE", "negative": "NEGATIVE"}


class Prediction(TypedDict):
    """Ce que l'API renvoie pour un texte."""

    label: Etiquette
    score: float
    text: str


class SentimentClassifier:
    """Enveloppe du modèle TP2 avec l'interface attendue par l'API."""

    model_name = "tfidf-logreg (TP2, models/sentiment.joblib)"

    def __init__(self) -> None:
        # échoue immédiatement si le joblib manque : on ne démarre pas sans modèle
        pipeline = charger_modele()
        inconnues = {str(c) for c in pipeline.classes_} - CORRESPONDANCE.keys()
        if inconnues:
            raise ValueError(f"classes du modèle hors contrat : {sorted(inconnues)}")

    def predict(self, text: str) -> Prediction:
        """Renvoie {'label': POSITIVE|NEGATIVE|INDETERMINE, 'score': float, 'text': aperçu}."""
        r = _predict(text)  # lève ValueError si le texte est vide
        label: Etiquette = CORRESPONDANCE[r["label"]]
        if r["score"] < SEUIL_ABSTENTION:
            label = "INDETERMINE"
        return {"label": label, "score": r["score"], "text": text[:100]}


def load_model() -> SentimentClassifier:
    """Construit le classifier (le cache de chargement est dans src/predict.py)."""
    return SentimentClassifier()
