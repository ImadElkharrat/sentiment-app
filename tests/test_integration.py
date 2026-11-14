"""Tests d'intégration : l'API telle qu'elle tourne vraiment (TP4, étape D).

Les tests du TP3 vérifient des réponses ; ceux-ci vérifient le démarrage de l'API
et son comportement quand le modèle manque ou tombe en panne.
"""
from pathlib import Path

import numpy as np
import pytest

MODELE = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"
pytestmark = pytest.mark.skipif(not MODELE.exists(), reason="modèle non produit : python src/train.py")

AVIS = {"text": "Livraison rapide, produit conforme, très satisfait"}


@pytest.fixture
def app():
    from api.main import app

    return app


@pytest.fixture
def cache_vide():
    """Vide le cache de chargement avant et après : aucun test n'hérite d'un modèle d'un autre."""
    import predict

    predict.charger_modele.cache_clear()
    yield predict
    predict.charger_modele.cache_clear()


def test_demarrage_reel_charge_le_modele():
    """D.1 : un client ouvert par « with » exécute le lifespan."""
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as client:
        reponse = client.get("/health")
    assert reponse.status_code == 200
    assert "TP2" in reponse.json()["model"]


def test_modele_absent_refus_de_demarrer(app, cache_vide, monkeypatch, tmp_path):
    """D.2 : sans fichier de modèle, l'API ne démarre pas (le contrôle T20, automatique)."""
    from fastapi.testclient import TestClient

    monkeypatch.setattr(cache_vide, "MODELE", tmp_path / "absent.joblib")
    with pytest.raises(FileNotFoundError, match="sentiment.joblib absent"):
        with TestClient(app):
            pass


def test_modele_non_charge_503(app):
    """D.3 : l'API démarrée, modèle retiré de app.state : 503 sur /health et /predict."""
    from fastapi.testclient import TestClient

    with TestClient(app) as client:
        mp = pytest.MonkeyPatch()
        mp.setattr(app.state, "classifier", None)
        try:
            assert client.get("/health").status_code == 503
            reponse = client.post("/predict", json=AVIS)
            assert reponse.status_code == 503
            assert reponse.json()["detail"] == "Modèle non chargé"
        finally:
            mp.undo()


class ModeleEnPanne:
    model_name = "en panne"

    def __init__(self, erreur: Exception) -> None:
        self.erreur = erreur

    def predict(self, text: str):
        raise self.erreur


@pytest.mark.parametrize("erreur", [RuntimeError("bug interne"), ValueError("bug interne")],
                         ids=["RuntimeError", "ValueError"])
def test_modele_en_panne_500(app, erreur):
    """D.4 : quelle que soit l'exception du modèle, 500, sans le message interne."""
    from fastapi.testclient import TestClient

    with TestClient(app) as client:
        mp = pytest.MonkeyPatch()
        mp.setattr(app.state, "classifier", ModeleEnPanne(erreur))
        try:
            reponse = client.post("/predict", json=AVIS)
        finally:
            mp.undo()
    assert reponse.status_code == 500
    assert "bug interne" not in reponse.text


class PipelineAutresClasses:
    """Un modèle dont les classes ne sont pas celles du contrat."""

    classes_ = np.array(["negative", "neutre", "positive"])


def test_classes_inconnues_refus_de_demarrer(app, cache_vide, monkeypatch):
    """E.3 : un modèle aux étiquettes hors contrat empêche l'API de démarrer."""
    from fastapi.testclient import TestClient

    import api.model

    monkeypatch.setattr(api.model, "charger_modele", lambda: PipelineAutresClasses())
    with pytest.raises(ValueError, match="neutre"):
        with TestClient(app):
            pass
