"""Compatibilité avec l'ancien module du TP2."""
import sys

from sentiment_app.predict import predict as _predict


def predict(texte: str) -> dict[str, float | str]:
    resultat = _predict(texte)
    label = resultat["label"]
    if label in {"POSITIVE", "NEGATIVE"}:
        label = label.lower()
    return {"label": label, "score": resultat["score"]}


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage : python src/predict.py <texte>")
        return 2
    resultat = predict(" ".join(sys.argv[1:]))
    print(f"{resultat['label']} (confiance {resultat['score']:.0%})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
