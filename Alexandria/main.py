#from Janelas.Sistema_Login import TelaLogin
from pathlib import Path
import subprocess
import sys



BASE_DIR = Path(__file__).resolve().parent
PASTA_USUARIO = BASE_DIR.parent
PASTA_BIBLIOTECA = PASTA_USUARIO / "Biblioteca"


def verificar_biblioteca():
    if not PASTA_BIBLIOTECA.exists():
        PASTA_BIBLIOTECA.mkdir(parents=True)

    return PASTA_BIBLIOTECA


def iniciar():
    verificar_biblioteca()

    main = BASE_DIR / "Janelas/Sistema_Login.py"

    subprocess.run([sys.executable, str(main)])

if __name__ == "__main__":
    iniciar()


#tasks em diante
