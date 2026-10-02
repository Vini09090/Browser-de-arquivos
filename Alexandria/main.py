from pathlib import Path
import subprocess
import sys
from Dados.Configurações import Configuracoes


BASE_DIR = Path(__file__).resolve().parent
PASTA_USUARIO = BASE_DIR.parent
PASTA_BIBLIOTECA = PASTA_USUARIO / "Biblioteca"


configuracoes = Configuracoes()


def verificar_biblioteca():
    PASTA_BIBLIOTECA.mkdir(parents=True, exist_ok=True)

    categorias = configuracoes.obter_categorias()

    for categoria in categorias:
        pasta = PASTA_BIBLIOTECA / categoria

        if not pasta.exists():
            pasta.mkdir()


def iniciar():
    verificar_biblioteca()

    main = BASE_DIR / "Janelas/Sistema_Login.py"

    subprocess.run([sys.executable, str(main)])


if __name__ == "__main__":
    iniciar()
