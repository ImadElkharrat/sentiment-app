# Fiche de cadrage : Ordonnances incomplètes en pharmacie

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)
Vérifier automatiquement que chaque ordonnance soumise en pharmacie contient tous les champs légaux obligatoires avant la délivrance des médicaments.

## Utilisateur final (obligatoire)
Les pharmaciens et préparateurs en pharmacie, qui reçoivent une alerte immédiate lorsqu'une mention obligatoire manque sur l'ordonnance.

## Approche retenue (obligatoire)

Cocher une seule case :

- [x] Règles métier
- [ ] Machine learning
- [ ] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)
(b) Les champs obligatoires d'une ordonnance (date, signature, posologie, identité du patient et du médecin) suivent une réglementation connue et stable, ce qui rend chaque blocage 100 % explicable et vérifiable par le pharmacien. (c) Le contrôle par règles métier s'exécute instantanément avec un coût par requête quasi nul. (d) Valider à tort une ordonnance incomplète engage la responsabilité légale et sanitaire de la pharmacie, ce qui exclut une boîte noire probabiliste.

## Données nécessaires et leur origine (obligatoire)
Champs structurés extraits des ordonnances numérisées ou électroniques (RPPS du prescripteur, date, nom du patient, médicaments, posologie) issus du logiciel de gestion de l'officine.

## Métrique de succès et seuil d'acceptation (obligatoire)
Rappel de 100 % sur les ordonnances réellement incomplètes (aucune ordonnance non conforme ne doit passer sans alerte) et taux de fausses alertes inférieur à 5 % sur un jeu de test.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)
Une ordonnance incomplète validée à tort expose le patient à un risque médical et la pharmacie à un refus de remboursement ; le pharmacien inspecte et valide systématiquement chaque ordonnance signalée.

## Risques éthiques ou de confidentialité (obligatoire)
Les ordonnances contiennent des données de santé hautement sensibles : le traitement doit être strictement local ou sur un serveur certifié HDS, sans aucun envoi à une API externe.

## Approche écartée et pourquoi (facultatif)
Modèle génératif seul ou Machine Learning : trop coûteux, non déterministes et inutiles puisque les critères de conformité légale sont fixes et explicites.