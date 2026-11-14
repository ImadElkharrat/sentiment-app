"""Tests du paquet installable (TP6) : le modèle déplaçable, l'API sans bricolage, la commande."""
import shutil
from pathlib import Path

import pytest

RACINE = Path(__file__).resolve().parents[1]
MODELE = RACINE / "models" / "sentiment.joblib"
AVIS = "Livraison rapide, produit conforme, très satisfait"


@pytest.fixture
def predict_mod():
    from sentiment_app import predict

    predict.charger_modele.cache_clear()
    yield predict
    predict.charger_modele.cache_clear()


@pytest.mark.skipif(not MODELE.exists(), reason="modèle non produit : python src/train.py")
def test_le_modele_se_place_ou_l_on_veut(predict_mod, monkeypatch, tmp_path):
    ailleurs = tmp_path / "ailleurs" / "mon-modele.joblib"
    ailleurs.parent.mkdir()
    shutil.copy(MODELE, ailleurs)
    monkeypatch.setenv("SENTIMENT_MODELE", str(ailleurs))
    assert predict_mod.chemin_modele() == ailleurs
    assert predict_mod.predict(AVIS)["label"] == "positive"

    predict_mod.charger_modele.cache_clear()
    monkeypatch.setenv("SENTIMENT_MODELE", str(tmp_path / "absent.joblib"))
    with pytest.raises(FileNotFoundError, match="modèle introuvable"):
        predict_mod.charger_modele()


def test_l_api_ne_bricole_plus_le_chemin_de_python():
    fautifs = [f.name for f in (RACINE / "api").glob("*.py") if "sys.path" in f.read_text(encoding="utf-8")]
    assert not fautifs, f"sys.path encore modifié dans : {fautifs}"


def test_version(capsys):
    from sentiment_app import __version__
    from sentiment_app.cli import main

    with pytest.raises(SystemExit) as fin:
        main(["--version"])
    assert fin.value.code == 0
    assert capsys.readouterr().out.strip() == f"sentiment-app {__version__}"


@pytest.mark.skipif(not MODELE.exists(), reason="modèle non produit : python src/train.py")
def test_commande_predict(predict_mod, capsys):
    from sentiment_app.cli import main

    assert main(["predict", AVIS]) == 0
    assert capsys.readouterr().out.split()[0] == "POSITIVE"
    assert main(["predict", "xqzvb wlkptr grombu"]) == 0
    assert capsys.readouterr().out.split()[0] == "INDETERMINE"


def test_commande_sans_modele_code_1(predict_mod, monkeypatch, tmp_path, capsys):
    from sentiment_app.cli import main

    monkeypatch.setenv("SENTIMENT_MODELE", str(tmp_path / "absent.joblib"))
    assert main(["predict", AVIS]) == 1
    assert "modèle introuvable" in capsys.readouterr().err
