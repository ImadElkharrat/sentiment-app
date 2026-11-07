# Semaine 3 : l'API, notes du binôme

> Deux questions, quelques phrases chacune. Répondez avec ce que vous avez observé, pas avec le cours.

## 1. Pourquoi l'API refuse-t-elle de démarrer sans `models/sentiment.joblib`, plutôt que de démarrer et de répondre 503 ?

L'API charge le modèle dans son `lifespan` avant d'accepter des requêtes ; si `models/sentiment.joblib` manque, le `FileNotFoundError` arrête le démarrage afin de ne pas présenter un service comme sain alors qu'il ne peut pas prédire. Le code 503 est réservé au cas où l'application fonctionnerait sans classifier chargé.

## 2. Un texte vide est refusé deux fois : par Pydantic, puis par `predict()`. Est-ce redondant ?

Ce n'est pas redondant : Pydantic protège le contrat HTTP, par exemple en refusant directement `""`, tandis que `predict()` reste protégé pour les appels internes et refuse aussi une chaîne composée uniquement d'espaces. Cette double validation garantit donc le même invariant à deux frontières différentes.
