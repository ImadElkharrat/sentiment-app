"""Tests d'intégration : l'API telle qu'elle tourne vraiment (TP4, étape D). À COMPLÉTER.

Les tests du TP3 vérifient des réponses ; ceux-ci vérifient le démarrage de l'API
et son comportement quand le modèle manque ou tombe en panne.
"""
from pathlib import Path

import pytest

MODELE = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"
pytestmark = pytest.mark.skipif(not MODELE.exists(), reason="modèle non produit : python src/train.py")


def test_demarrage_reel_charge_le_modele():
    """D.1 (donné en exemple) : un client ouvert par « with » exécute le lifespan."""
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as client:
        reponse = client.get("/health")
    assert reponse.status_code == 200
    assert "TP2" in reponse.json()["model"]


def test_modele_absent_refuse_le_demarrage(monkeypatch, tmp_path):
    import importlib

    from fastapi.testclient import TestClient

    from api.main import app

    predict = importlib.import_module("sentiment_app.predict")
    monkeypatch.setattr(predict, "MODELE", tmp_path / "absent.joblib")
    predict.charger_modele.cache_clear()
    with pytest.raises(FileNotFoundError):
        with TestClient(app):
            pass
    predict.charger_modele.cache_clear()


def test_modele_non_charge_repond_503(monkeypatch):
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as client:
        monkeypatch.setattr(app.state, "classifier", None)
        assert client.get("/health").status_code == 503
        assert client.post("/predict", json={"text": "Très bien"}).status_code == 503


@pytest.mark.parametrize("exception", [RuntimeError("panne"), ValueError("bug interne")])
def test_panne_du_modele_repond_500(monkeypatch, exception):
    from fastapi.testclient import TestClient

    from api.main import app

    class BrokenClassifier:
        model_name = "modèle de test"

        def predict(self, _text: str):
            raise exception

    with TestClient(app) as client:
        monkeypatch.setattr(app.state, "classifier", BrokenClassifier())
        reponse = client.post("/predict", json={"text": "Très bien"})
        assert reponse.status_code == 500
        assert "bug interne" not in reponse.text
        assert "panne" not in reponse.text


def test_classes_inattendues_refusent_le_demarrage(monkeypatch):
    from api.model import SentimentClassifier

    class UnexpectedPipeline:
        classes_ = ["negative", "positive", "neutral"]

    monkeypatch.setattr("api.model.charger_modele", lambda: UnexpectedPipeline())
    with pytest.raises(ValueError, match="classes de modèle inattendues"):
        SentimentClassifier()
