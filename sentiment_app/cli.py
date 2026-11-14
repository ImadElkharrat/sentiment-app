"""La commande « sentiment », créée par pip à partir de [project.scripts] (TP6).

  sentiment --version
  sentiment predict "Livraison rapide, produit conforme, très satisfait"
  sentiment serve [--host 127.0.0.1] [--port 8000]
"""
import argparse
import sys

from sentiment_app import __version__


def _predict(texte: str) -> int:
    # Même chemin que l'API : seuil d'abstention et étiquettes du contrat compris.
    from api.model import load_model

    try:
        classifier = load_model()
    except FileNotFoundError as erreur:
        print(erreur, file=sys.stderr)
        return 1
    try:
        resultat = classifier.predict(texte)
    except ValueError as erreur:
        print(f"texte refusé : {erreur}", file=sys.stderr)
        return 2
    print(f"{resultat['label']} {resultat['score']}")
    return 0


def _serve(host: str, port: int) -> int:
    import uvicorn

    uvicorn.run("api.main:app", host=host, port=port, log_level="info")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="sentiment", description="Analyse de sentiment des avis.")
    parser.add_argument("--version", action="version", version=f"sentiment-app {__version__}")
    commandes = parser.add_subparsers(dest="commande", required=True)

    p_predict = commandes.add_parser("predict", help="classer un avis")
    p_predict.add_argument("texte", nargs="+", help="le texte de l'avis")

    p_serve = commandes.add_parser("serve", help="lancer l'API (uvicorn)")
    p_serve.add_argument("--host", default="127.0.0.1")
    p_serve.add_argument("--port", type=int, default=8000)

    args = parser.parse_args(argv)
    if args.commande == "predict":
        return _predict(" ".join(args.texte))
    return _serve(args.host, args.port)


if __name__ == "__main__":
    raise SystemExit(main())
