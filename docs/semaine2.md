# Semaine 2 — Analyse des erreurs

Les erreurs sont des avis mitigés qui changent de sens après « sauf que ensuite » : deux positifs prédits négatifs, un négatif prédit positif.
Le sac de mots compte les mots positifs et négatifs sans voir leur ordre, donc il rate le retournement final.
Il faudrait un modèle qui tient compte de l'ordre, par exemple avec des n-grammes (« sauf que ») ou un modèle comme CamemBERT.
