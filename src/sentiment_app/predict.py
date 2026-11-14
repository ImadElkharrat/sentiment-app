"""Prédiction de sentiment indépendante du dossier courant."""
import os
from functools import lru_cache
from pathlib import Path
from typing import Literal, TypedDict

import joblib

ContractLabel = Literal["POSITIVE", "NEGATIVE", "INDETERMINE"]
ModelLabel = Literal["positive", "negative"]
SEUIL_ABSTENTION = 0.60
MODELE = Path(__file__).resolve().parents[2] / "models" / "sentiment.joblib"


class Resultat(TypedDict):
    label: ContractLabel
    score: float


def _chemin_modele() -> Path:
    configured = os.environ.get("SENTIMENT_MODELE")
    return Path(configured) if configured else MODELE


@lru_cache(maxsize=1)
def charger_modele():
    chemin = _chemin_modele()
    if not chemin.exists():
        raise FileNotFoundError(
            "modèle introuvable : définissez SENTIMENT_MODELE vers models/sentiment.joblib"
        )
    return joblib.load(chemin)


def _label_modele(value: object) -> ModelLabel:
    if value == "positive":
        return "positive"
    if value == "negative":
        return "negative"
    raise ValueError(f"étiquette de modèle inconnue : {value!r}")


def predict(texte: str) -> Resultat:
    """Renvoie une étiquette du contrat et applique le seuil d'abstention."""
    if not isinstance(texte, str) or not texte.strip():
        raise ValueError("texte vide")
    modele = charger_modele()
    etiquette = _label_modele(modele.predict([texte])[0])
    score = round(float(modele.predict_proba([texte]).max()), 4)
    if score < SEUIL_ABSTENTION:
        label: ContractLabel = "INDETERMINE"
    else:
        label = "POSITIVE" if etiquette == "positive" else "NEGATIVE"
    return {"label": label, "score": score}
