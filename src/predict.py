#!/usr/bin/env python
"""Fichier de compatibilité (TP6) : le code vit désormais dans sentiment_app/predict.py.

Les anciennes habitudes continuent de fonctionner :
  python src/predict.py "Livraison rapide, très satisfait"
  >>> from predict import predict
Aucune logique ici : tout est délégué au paquet (installé par pip install -e .).
"""
from sentiment_app.predict import (  # noqa: F401  (réexportés pour les anciens imports)
    MODELE,
    Resultat,
    charger_modele,
    chemin_modele,
    main,
    predict,
)

if __name__ == "__main__":
    raise SystemExit(main())
