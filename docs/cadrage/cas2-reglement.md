# Fiche de cadrage : Questions sur le règlement intérieur

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)
Fournir aux étudiants et au personnel des réponses précises et sourcées aux questions portant sur le règlement intérieur de l'école.

## Utilisateur final (obligatoire)
Les étudiants, les enseignants et l'administration de l'école qui cherchent rapidement un point de règlement (absences, examens, discipline).

## Approche retenue (obligatoire)

Cocher une seule case :

- [ ] Règles métier
- [ ] Machine learning
- [x] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)
(a) L'école dispose déjà des documents officiels du règlement intérieur mais n'a pas de jeu de milliers de questions-réponses étiquetées pour entraîner un classifieur supervisé. (b) La vérifiabilité est indispensable : l'approche RAG permet de citer l'article et la page exacte du règlement pour que l'étudiant puisse vérifier la réponse. (d) Une réponse inventée (hallucination) induirait un étudiant en erreur sur ses droits ou obligations académiques.

## Données nécessaires et leur origine (obligatoire)
Textes officiels à jour du règlement intérieur, chartes des examens et guides étudiants au format PDF ou Markdown, fournis par la direction des études.

## Métrique de succès et seuil d'acceptation (obligatoire)
Taux de réponses correctement sourcées (citation du bon article sans hallucination) d'au moins 90 % sur un jeu d'évaluation de 50 questions types validées par la scolarité.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)
Une mauvaise interprétation peut entraîner un litige sur une sanction ou une absence ; chaque réponse affiche le passage officiel source et renvoie vers le service de scolarité en cas de doute.

## Risques éthiques ou de confidentialité (obligatoire)
Les utilisateurs pourraient saisir des informations personnelles (santé, situation familiale) dans leurs questions : les requêtes ne doivent pas être conservées avec l'identité de l'étudiant.

## Approche écartée et pourquoi (facultatif)
Modèle génératif seul sans RAG : il ne connaît pas le règlement propre à l'école et inventerait des règles inexistantes sans pouvoir citer l'article officiel.