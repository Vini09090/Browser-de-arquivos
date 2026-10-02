
from pathlib import Path
import subprocess
import sys

BASE_DIR = Path(__file__).resolve().parent
PASTA_USUARIO = BASE_DIR.parent
PASTA_BIBLIOTECA = PASTA_USUARIO / "Biblioteca"

CATEGORIAS = [
    "Matematica",
    "Literatura",
    "Historia",
    "Programacao",
    "Filosofia",
    "Ciencia"
]


def verificar_biblioteca():
    PASTA_BIBLIOTECA.mkdir(parents=True, exist_ok=True)

    for categoria in CATEGORIAS:
        pasta = PASTA_BIBLIOTECA / categoria

        if not pasta.exists():
            pasta.mkdir()


def iniciar():
    verificar_biblioteca()

    main = BASE_DIR / "Janelas/Sistema_Login.py"

    subprocess.run([sys.executable, str(main)])


if __name__ == "__main__":
    iniciar()
