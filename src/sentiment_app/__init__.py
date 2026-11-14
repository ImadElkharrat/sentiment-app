"""Paquet public de classification de sentiment."""
from importlib.metadata import PackageNotFoundError, version

from sentiment_app.predict import predict

try:
    __version__ = version("sentiment-app")
except PackageNotFoundError:
    __version__ = "0.6.0"

__all__ = ["__version__", "predict"]
