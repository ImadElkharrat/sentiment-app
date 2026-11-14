# sentiment-app

Paquet Python et commande en ligne pour classer des avis clients en français.

## Installation

```powershell
pip install sentiment_app-0.6.0-py3-none-any.whl
```

Le modèle n'est pas inclus dans la roue. Définissez `SENTIMENT_MODELE` vers un
fichier `sentiment.joblib` compatible avant d'utiliser la commande.

## Utilisation

```powershell
$env:SENTIMENT_MODELE = "C:\Users\imade\OneDrive\Desktop\EMSI\5IIR_S9\DAI\sentiment-app\models\sentiment.joblib"
sentiment predict "Livraison rapide, produit conforme"
sentiment predict "xqzvb wlkptr grombu" --json
```

Le modèle renvoie `POSITIVE`, `NEGATIVE` ou `INDETERMINE` lorsque sa confiance
est inférieure à 0,60. Les fichiers Joblib doivent provenir d'une source de
confiance, car leur chargement peut exécuter du code.

## Limites

Le modèle TF-IDF dépend de son jeu d'entraînement et comprend mal l'ironie, les
négations complexes et les domaines éloignés des avis d'origine. Une abstention
doit être vérifiée par un humain.
