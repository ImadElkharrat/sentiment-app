# Semaine 5 : l'interface, notes du binôme

## 1. Pourquoi l'interface n'importe-t-elle jamais `predict()` ni le fichier `.joblib` ?

La page ne connaît que `ui.client`, qui ne connaît que l'adresse de l'API et ses codes de réponse.
Nous l'avons vérifié en arrêtant l'API : la page n'a plus rien à afficher que « API injoignable », car
elle n'a aucun autre accès au modèle. Le modèle, le seuil d'abstention (0,60) et la correspondance des
étiquettes restent donc à un seul endroit, l'API. Réentraîner le modèle ou changer le seuil ne demande
aucune modification de la page, et l'API reste la seule porte d'entrée, que les agents du TP10
partageront.

## 2. Que montre l'interface quand le modèle hésite, et pourquoi est-ce mieux qu'un verdict forcé ?

Pour « xqzvb wlkptr grombu », la page affiche « Je ne sais pas : à faire vérifier par un humain »,
avec 52 %, et l'encadré « La confiance est sous le seuil d'abstention : un humain doit trancher ».
Avant le TP4, le même texte recevait « négatif » à 52 %. C'était un verdict sans aucune information,
puisqu'aucun mot n'est connu du modèle, mais présenté comme les autres. L'abstention dit la vérité sur
la confiance et envoie l'avis à quelqu'un qui peut le lire, au lieu de ranger un client parmi les
mécontents par erreur.

## 3. Que voit l'utilisateur quand l'API tombe ? Et le fichier `data/avis_exemple.csv` : combien d'avis partent vers un humain ?

API arrêtée, la page affiche en haut, dès le rechargement et avant toute analyse, « API injoignable :
lancez d'abord uvicorn api.main:app ». Ce n'est pas une trace Python, parce que le client traduit
l'échec de connexion en message. Trois espaces donnent l'avertissement « Texte refusé : vide, fait
d'espaces, ou de plus de 2000 caractères. » (réponse 422 de l'API).

Pour `data/avis_exemple.csv`, le résumé est `{'INDETERMINE': 1, 'NEGATIVE': 2, 'POSITIVE': 3}`. Un seul
avis sur six part vers un humain, « xqzvb wlkptr grombu » (0,5162). « Pas déçu du tout, je recommande »
passe de justesse, en positif à 0,618, juste au-dessus du seuil.
