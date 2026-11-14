# Semaine 5 : l'interface, notes du binôme

> Trois questions, quelques phrases chacune. Répondez avec ce que vous avez observé.

## 1. Pourquoi l'interface n'importe-t-elle jamais `predict()` ni le fichier `.joblib` ?

L'interface appelle uniquement `ui.client`, qui envoie les requêtes HTTP à
l'API. Le modèle reste donc chargé et exécuté dans le service ; un réentraînement
ne demande aucune modification de Streamlit.

## 2. Que montre l'interface quand le modèle hésite, et pourquoi est-ce mieux qu'un verdict forcé ?

Pour un texte inconnu, elle affiche « Je ne sais pas : à faire vérifier par un
humain », avec la confiance de 52 % et le message indiquant que le score est
sous le seuil d'abstention. C'est préférable à un verdict arbitraire, car
l'incertitude est visible et la décision peut être revue par un agent.

## 3. Que voit l'utilisateur quand l'API tombe ? Et le fichier `data/avis_exemple.csv` : combien d'avis partent vers un humain ?

Il voit « API injoignable : lancez d'abord uvicorn api.main:app », sans
traceback technique. Le fichier contient six avis : trois positifs, deux
négatifs et un avis `INDETERMINE` envoyé à un humain.
