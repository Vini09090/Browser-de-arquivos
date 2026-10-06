import subprocess
import sys
from pathlib import Path
from Dados.Configurações import Configuracoes

# Instancia as configurações
configuracoes = Configuracoes()

# Diretório base do script atual
BASE_DIR = Path(__file__).resolve().parent

# Define a pasta da biblioteca usando a Home do computador/configurações
PASTA_BIBLIOTECA = configuracoes.obter_pasta_biblioteca()


def verificar_biblioteca():
    # Cria a pasta da biblioteca se não existir
    PASTA_BIBLIOTECA.mkdir(parents=True, exist_ok=True)

    categorias = configuracoes.obter_categorias()

    for categoria in categorias:
        pasta = PASTA_BIBLIOTECA / categoria
        if not pasta.exists():
            pasta.mkdir(parents=True, exist_ok=True)


def iniciar():
    verificar_biblioteca()

    main = BASE_DIR / "Janelas" / "Sistema_Login.py"

    subprocess.run([sys.executable, str(main)])


if __name__ == "__main__":
    iniciar()
