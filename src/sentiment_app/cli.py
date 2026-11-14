"""Commande « sentiment »."""
import argparse
import json
import sys

from sentiment_app import __version__
from sentiment_app.predict import predict


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="sentiment")
    parser.add_argument("--version", action="version", version=f"sentiment-app {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)

    predict_parser = commands.add_parser("predict", help="classer un avis")
    predict_parser.add_argument("texte", nargs="+")
    predict_parser.add_argument("--json", action="store_true", help="sortie JSON")

    serve_parser = commands.add_parser("serve", help="lancer l'API FastAPI")
    serve_parser.add_argument("--host", default="127.0.0.1")
    serve_parser.add_argument("--port", type=int, default=8000)

    args = parser.parse_args(argv)
    if args.command == "serve":
        import uvicorn

        uvicorn.run("api.main:app", host=args.host, port=args.port, log_level="info")
        return 0

    try:
        resultat = predict(" ".join(args.texte))
    except (FileNotFoundError, ValueError) as error:
        print(f"erreur : {error}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(resultat, ensure_ascii=False))
    else:
        print(f"{resultat['label']} (confiance {resultat['score']:.0%})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
