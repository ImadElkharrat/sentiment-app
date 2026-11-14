#!/usr/bin/env python
"""Prédiction unitaire : la fonction que l'API appelle (TP2, placée dans le paquet au TP6).

Le modèle se trouve, dans l'ordre :
  1. au chemin donné par la variable d'environnement SENTIMENT_MODELE ;
  2. sinon dans models/sentiment.joblib, à la racine du dépôt.
Installé par la roue, hors du dépôt, le paquet a donc besoin de SENTIMENT_MODELE.
"""
import os
import sys
from functools import lru_cache
from pathlib import Path
from typing import Literal, TypedDict

import joblib

VARIABLE = "SENTIMENT_MODELE"
MODELE = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"


class Resultat(TypedDict):
    """Le retour de predict() : l'étiquette du modèle, en minuscules, et sa confiance."""

    label: Literal["positive", "negative"]
    score: float


def chemin_modele() -> Path:
    """Le chemin du modèle : SENTIMENT_MODELE s'il est défini, sinon celui du dépôt."""
    valeur = os.environ.get(VARIABLE, "").strip()
    return Path(valeur) if valeur else MODELE


@lru_cache(maxsize=1)
def charger_modele():
    """Chargé une seule fois par processus, pas à chaque appel."""
    chemin = chemin_modele()
    if not chemin.exists():
        raise FileNotFoundError(
            f"modèle introuvable : {chemin} absent. Lancez python src/train.py dans le dépôt, "
            f"ou indiquez le chemin du fichier .joblib dans la variable {VARIABLE}."
        )
    return joblib.load(chemin)


def predict(texte: str) -> Resultat:
    """Renvoie {'label': 'positive'|'negative', 'score': float}."""
    if not isinstance(texte, str) or not texte.strip():
        raise ValueError("texte vide")
    pipeline = charger_modele()
    etiquette = pipeline.predict([texte])[0]
    score = float(pipeline.predict_proba([texte]).max())
    return {"label": etiquette, "score": round(score, 4)}


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    resultat = predict(" ".join(sys.argv[1:]))
    print(f"{resultat['label']} (confiance {resultat['score']:.0%})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
