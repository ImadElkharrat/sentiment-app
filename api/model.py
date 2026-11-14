"""Raccord entre l'API et le paquet installable de sentiment."""
from typing import Literal, TypedDict

from sentiment_app.predict import charger_modele
from sentiment_app.predict import predict as _predict

ContractLabel = Literal["POSITIVE", "NEGATIVE", "INDETERMINE"]
MODEL_LABELS = {"positive", "negative"}


class ApiPrediction(TypedDict):
    label: ContractLabel
    score: float
    text: str


class SentimentClassifier:
    """Enveloppe du modèle TP2 avec l'interface attendue par l'API."""

    model_name = "tfidf-logreg (TP2, models/sentiment.joblib)"

    def __init__(self) -> None:
        pipeline = charger_modele()
        classes = set(getattr(pipeline, "classes_", []))
        if not classes or not classes.issubset(MODEL_LABELS):
            raise ValueError(f"classes de modèle inattendues : {sorted(classes)!r}")

    def predict(self, text: str) -> ApiPrediction:
        """Renvoie {'label': 'POSITIVE'|'NEGATIVE', 'score': float, 'text': aperçu}."""
        r = _predict(text)  # lève ValueError si le texte est vide
        return {"label": r["label"], "score": r["score"], "text": text[:100]}


def load_model() -> SentimentClassifier:
    """Construit le classifier (le cache de chargement est dans src/predict.py)."""
    return SentimentClassifier()
