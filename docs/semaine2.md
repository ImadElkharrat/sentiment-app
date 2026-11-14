# Semaine 2 — Analyse des erreurs

Les erreurs sont des avis mitigés qui changent de sens après « sauf que ensuite » : deux positifs prédits négatifs, un négatif prédit positif.
Le sac de mots compte les mots positifs et négatifs sans voir leur ordre, donc il rate le retournement final.
Les bigrammes du vectoriseur ne suffisent pas, car le retournement porte sur toute la phrase : il faudrait une représentation qui tient compte de l'ordre et du contexte des mots, comme des embeddings de phrase ou un modèle comme CamemBERT.
