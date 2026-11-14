"""Vérifie la roue TP6 dans un environnement Python neuf."""
import os
import subprocess
import tempfile
import venv
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.6.0"


def noter(ok: bool, message: str, detail: str = "") -> bool:
    print(f"[{'OK' if ok else 'CHEC'}] {message}" + (f" : {detail}" if detail else ""))
    return ok


def run(command: list[str], cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True, check=False)


def main() -> int:
    dist = ROOT / "dist"
    wheels = sorted(dist.glob(f"sentiment_app-{VERSION}-*.whl"))
    sdists = sorted(dist.glob(f"sentiment_app-{VERSION}.tar.gz"))
    ok = True
    ok &= noter(len(wheels) == 1, "roue présente")
    ok &= noter(len(sdists) == 1, "distribution source présente")
    if not wheels or not sdists:
        return terminer(ok)

    with zipfile.ZipFile(wheels[0]) as archive:
        names = archive.namelist()
    package_files = {name.split("/")[0] for name in names if "/" in name}
    ok &= noter("sentiment_app" in package_files, "paquet sentiment_app dans la roue")
    ok &= noter("api" in package_files and "ui" in package_files, "API et interface dans la roue")
    ok &= noter(not any(name.startswith("tests/") for name in names), "pas de tests dans la roue")
    ok &= noter(not any(name.endswith(".joblib") for name in names), "pas de modèle dans la roue")
    ok &= noter(f"[{VERSION}]" in (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"),
                "CHANGELOG décrit la version")

    with tempfile.TemporaryDirectory() as temporary:
        directory = Path(temporary)
        venv.create(directory / "env", with_pip=True)
        binaries = directory / "env" / ("Scripts" if os.name == "nt" else "bin")
        python = binaries / ("python.exe" if os.name == "nt" else "python")
        environment = {
            **os.environ,
            "VERIFICATION_LIVRABLE": "1",
            "SENTIMENT_MODELE": str(ROOT / "models" / "sentiment.joblib"),
        }
        installed = run([str(python), "-m", "pip", "install", "-q", str(wheels[0])], directory, environment)
        ok &= noter(installed.returncode == 0, "installation dans un environnement neuf",
                    installed.stderr.strip().splitlines()[-1] if installed.returncode else "")
        tests = run(
            [str(python), "-m", "pip", "install", "-q", "pytest"],
            directory,
            environment,
        )
        ok &= noter(tests.returncode == 0, "installation de pytest")
        if tests.returncode == 0:
            result = run(
                [str(python), "-m", "pytest", "-q", "-p", "no:cacheprovider",
                 "-o", "pythonpath=", str(ROOT / "tests" / "test_paquet.py")],
                directory,
                environment,
            )
            ok &= noter(result.returncode == 0, "tests du paquet installé",
                        result.stdout.strip().splitlines()[-1] if result.stdout else result.stderr)
            command = binaries / ("sentiment.exe" if os.name == "nt" else "sentiment")
            cli = run([str(command), "--version"], directory, environment)
            ok &= noter(cli.returncode == 0 and cli.stdout.strip() == f"sentiment-app {VERSION}",
                        "commande sentiment installée", cli.stdout.strip() or cli.stderr.strip())
    return terminer(ok)


def terminer(ok: bool) -> int:
    rapport = ROOT / "docs" / "livrable-tp4.txt"
    rapport.write_text(f"Bilan : {'CONFORME' if ok else 'À CORRIGER'}\n", encoding="utf-8")
    print(f"Bilan : {'CONFORME' if ok else 'À CORRIGER'}")
    print(f"Rapport : {rapport.relative_to(ROOT)}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
