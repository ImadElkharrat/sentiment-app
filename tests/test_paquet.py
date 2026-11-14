"""Tests exécutés contre le paquet installé par le vérificateur TP6."""
import importlib.util
import os
import shutil
import subprocess
import sys

import pytest

_spec = importlib.util.find_spec("sentiment_app")
if not (_spec and "site-packages" in (_spec.origin or "")) and not os.environ.get(
    "VERIFICATION_LIVRABLE"
):
    pytest.skip("paquet non installé : lancer scripts/verifier_livrable.py", allow_module_level=True)

import sentiment_app  # noqa: E402


def test_importe_depuis_le_paquet_installe():
    assert "site-packages" in sentiment_app.__file__


def test_version():
    assert sentiment_app.__version__ == "0.6.0"


def test_prediction_avec_modele():
    resultat = sentiment_app.predict("Livraison rapide, produit conforme, très satisfait")
    assert resultat["label"] == "POSITIVE"
    assert 0 <= resultat["score"] <= 1


def test_abstention_avec_texte_inconnu():
    resultat = sentiment_app.predict("xqzvb wlkptr grombu")
    assert resultat["label"] == "INDETERMINE"


def test_commande_installee():
    commande = shutil.which("sentiment", path=os.path.dirname(sys.executable))
    assert commande
    resultat = subprocess.run(
        [commande, "--version"], capture_output=True, text=True, check=False
    )
    assert resultat.returncode == 0
    assert resultat.stdout.strip() == "sentiment-app 0.6.0"
