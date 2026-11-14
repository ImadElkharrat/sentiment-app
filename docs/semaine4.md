# Semaine 4 : tests approfondis et qualité, notes du binôme

## 1. Couverture

- Avant (étape A) : 91 % pour `api/`, 6 lignes jamais exécutées, toutes dans `main.py` : 49, 77-79, 85-87.
- Ce que ces lignes représentaient :
  - ligne 49 : le 503 quand le modèle n'est pas chargé, aucun test ne retirait le modèle ;
  - lignes 77-79 : le 500 quand le modèle plante en pleine requête, aucun test ne simulait de panne ;
  - lignes 85-87 : le lancement direct `python api/main.py`, qui ne tourne jamais sous pytest.
- Après (étape D) : 97,8 % (`Required test coverage of 95% reached`). Seul le bloc
  `if __name__ == "__main__":` reste non couvert. Nous n'avons rien exclu de la mesure : le seuil de 95 %
  est atteint sans `# pragma: no cover`.

## 2. Défauts trouvés

| Symptôme | Test qui l'a révélé | Correction |
| --- | --- | --- |
| `{"text": "   "}` reçoit 422, mais `detail` est une chaîne (`"texte vide"`, venue de `predict()`), alors que `{"text": ""}` reçoit la liste standard de Pydantic | `test_frontieres_du_contrat[espaces-seuls]` et la propriété `test_propriete_blancs_refuses` (contre-exemple minimal d'hypothesis : `texte=' '`) | `field_validator` dans `api/schemas.py`, même règle que `predict()` : `str.strip()`. Cas `\x85` ajouté au test paramétré, car `strip()` retire aussi ce blanc Unicode |
| Un texte de mots inventés reçoit `NEGATIVE` avec 0,5162 de confiance : un verdict forcé, sans aucune information | essai dans `/docs` (trois textes, même score), puis `src/courbe_seuil.py` | abstention : sous `SEUIL_ABSTENTION = 0.60`, l'étiquette devient `INDETERMINE` |
| Une panne `ValueError("bug interne")` du modèle répondait 422 avec le message interne, comme si le client s'était trompé | `test_modele_en_panne_500[ValueError]` (`assert 422 == 500`) | conversion de `ValueError` en 422 retirée de `main.py` : toute panne répond 500 |
| `.upper()` fabriquait l'étiquette sans contrôle : un modèle à trois classes aurait renvoyé `NEUTRE`, hors contrat | `mypy api`, une fois `predict()` typé en `TypedDict` + `Literal` | correspondance explicite `CORRESPONDANCE`, classes vérifiées au démarrage (`test_classes_inconnues_refus_de_demarrer`) |
| « Ce n'est pas un mauvais produit, bien au contraire » est classé `NEGATIVE` | `test_pas_d_erreur_franche[ligne-15]` (jeu d'or) | gardé dans le jeu, déclaré en `xfail(strict=True)` : le sac de mots ne voit pas que deux négations s'annulent |

## 3. Seuil d'abstention

Courbe sur les 58 avis de test du jeu de démonstration :

| Seuil | Répond à | Exactitude | Erreurs | Vers un humain |
| --- | --- | --- | --- | --- |
| 0,50 | 58 (100 %) | 0,879 | 7 | 0 |
| 0,60 | 42 (72 %) | 0,952 | 2 | 16 |
| 0,70 | 37 (64 %) | 1,000 | 0 | 21 |

Nous retenons 0,60. 16 avis sur 58 (28 %) partent vers un humain, et 5 des 7 erreurs sont évitées.
Passer à 0,70 éviterait les 2 dernières erreurs, mais au prix de 5 renvois de plus. Au-delà, le modèle
ne répond presque plus : 22 % des avis à 0,80.

## 4. Jeu d'or

- Bilan (`python src/bilan_jeu_or.py`) : 14 justes, 5 abstentions, 1 erreur franche déclarée, sur
  20 avis dont 8 difficiles.
- `pytest tests/test_jeu_or.py` : 20 passed, 1 xfailed.
- Ce que ces chiffres disent du modèle : les 12 avis simples sont justes, sauf un qui part en abstention.
  Les difficultés se répartissent ainsi :
  - les 2 avis d'un autre domaine (film, hôtel) partent en abstention : le vocabulaire est hors
    entraînement, et l'abstention nous protège ici ;
  - les avis mitigés partent aussi en abstention, au lieu des erreurs franches vues au TP2 ;
  - l'ironie (« bravo le transporteur ») passe, parce que les mots « cassé » et « perdue » portent le
    sens ;
  - la double négation reste une erreur franche, que seule une représentation qui tient compte de
    l'ordre des mots pourrait corriger.

## 5. Outils statiques

- Remarques au départ : ruff 11 (B904 ×2 dans `main.py`, I001 et F401 dans `model.py`, F401 et B905 ×2
  dans `evaluate.py`, I001 dans `test_api.py`, E741 ×3 dans les tests du TP1) ; mypy 0.
- Parmi les 5 défauts de la partie 2, ruff n'en a signalé aucun. B904 portait sur les deux `raise` du
  bloc fautif, mais il réclamait un `from`, pas un autre code de réponse. mypy n'en a trouvé qu'un
  (`.upper()`), et seulement après que nous avons typé le contrat : avec un `dict` sans précision, il ne
  voyait que des `Any`.
- Conclusion : les outils statiques trouvent les maladresses de code, pas les erreurs de comportement.
  Ces dernières ont été trouvées par des tests qui posent la bonne question (frontières, propriétés,
  pannes, jeu d'or). ruff et mypy ont leur place dans le crochet et dans la CI parce qu'ils ne coûtent
  rien, mais ils ne remplacent aucun test.
