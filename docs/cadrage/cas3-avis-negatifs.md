# Fiche de cadrage : Priorisation des avis négatifs

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)
Classer automatiquement les milliers d'avis clients reçus sur le site e-commerce afin d'isoler et de traiter en priorité les avis négatifs.

## Utilisateur final (obligatoire)
L'équipe du service client (Customer Success), qui consulte une file d'attente priorisant les avis négatifs au lieu de lire tous les commentaires manuellement.

## Approche retenue (obligatoire)

Cocher une seule case :

- [ ] Règles métier
- [x] Machine learning
- [ ] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)
(a) L'historique des milliers d'avis passés avec leurs notes et étiquettes fournit un large jeu de données étiquetées idéal pour l'apprentissage supervisé. (c) Avec des milliers d'avis par jour, un classifieur ML classique (TF-IDF + régression logistique ou petit modèle) offre un coût par requête très faible et une latence de quelques millisecondes, contrairement à un LLM. (b) Chaque prédiction reste vérifiable en un coup d'œil par l'agent qui lit l'avis remonté.

## Données nécessaires et leur origine (obligatoire)
Historique exporté en CSV depuis la base de données du site e-commerce contenant le texte des avis clients et le label de sentiment (positif ou négatif), préalablement anonymisé.

## Métrique de succès et seuil d'acceptation (obligatoire)
Score F1 macro d'au moins 0,85 sur le jeu de test, avec un rappel supérieur à 0,90 sur la classe des avis négatifs pour manquer le moins possible de clients mécontents.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)
Un faux négatif retarde la prise en charge d'un client insatisfait tandis qu'un faux positif est simplement reclassé en un clic par l'agent du support, ce qui enrichit la base de réentraînement.

## Risques éthiques ou de confidentialité (obligatoire)
Les avis peuvent contenir des noms, numéros de commande ou données personnelles : une étape d'anonymisation (suppression des données identifiantes) est appliquée avant l'entraînement et le stockage.

## Approche écartée et pourquoi (facultatif)
Règles métier par mots-clés : trop fragiles face aux fautes d'orthographe, aux négations ("pas bon") et à l'ironie présente dans les avis clients.