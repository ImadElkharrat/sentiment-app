# Semaine 4 : tests approfondis et qualité, notes du binôme

> Une à deux pages. Uniquement des chiffres issus de VOS exécutions.

## 1. Couverture

- Avant (étape A) : 92,75 %, lignes jamais exécutées : `api/main.py` 77-79 et
  85-87. Les premières correspondaient aux erreurs de prédiction et les secondes
  au lancement direct par Uvicorn.
- Après (étape D) : 97,83 %. Les seules lignes encore non exécutées sont le
  lancement direct par Uvicorn (`api/main.py` 85-87) ; aucune ligne n'a été
  artificiellement exclue de la mesure.

## 2. Défauts trouvés

| Symptôme | Test qui l'a révélé | Correction |
| --- | --- | --- |
| Un texte composé d'espaces était accepté | `test_frontieres_du_contrat` et `test_tout_texte_blanc_est_refuse` | Validation Pydantic avec `strip()` dans `PredictRequest` |
| Un texte inconnu recevait un verdict forcé à 52 % | `test_texte_inconnu_donne_indetermine` | Seuil nommé `SEUIL_ABSTENTION = 0.60` |
| Une panne `ValueError` était renvoyée en 422 | `test_panne_du_modele_repond_500` | Les erreurs du modèle sont désormais des réponses 500 |
| Les classes d'un modèle incompatible n'étaient pas vérifiées | `test_classes_inattendues_refusent_le_demarrage` | Validation explicite des classes au démarrage |

## 3. Seuil d'abstention

- À 0,50, le modèle répond à 100 % des avis avec une exactitude de 0,879.
  À 0,60, il répond à 72 % avec une exactitude de 0,952. À 0,70, il répond
  à 64 % avec une exactitude de 1,000.
- Seuil retenu : 0,60 ; 16 avis sur 58 (28 %) sont envoyés à un humain.
  Ce compromis améliore nettement l'exactitude tout en laissant une majorité
  d'avis traités automatiquement.

## 4. Jeu d'or

- Bilan (`python src/bilan_jeu_or.py`) : 14 avis justes, 5 abstentions et
  1 erreur franche déclarée sur 20 avis.
- Le seuil évite quatre erreurs franches supplémentaires sur les avis difficiles.
  Le modèle reste performant sur les avis explicites, mais l'ironie, la
  négation et le changement de domaine nécessitent une vérification humaine.

## 5. Outils statiques

- Au départ, Ruff signalait 23 remarques et mypy n'en signalait aucune sur
  l'API. Après correction du code du projet et exclusion des kits pédagogiques,
  `ruff check .` et `mypy api` sont silencieux.
- Ruff avait signalé des problèmes de qualité de code, mais ni Ruff ni mypy
  n'avaient détecté les défauts fonctionnels de validation, d'abstention ou de
  gestion du modèle. Les tests de comportement restent donc indispensables.
