import json
from pathlib import Path

class Configuracoes:
    def __init__(self, arquivo=None):
        # Define a pasta Home do sistema e a pasta padrão para o app
        self.home_usuario = Path.home()
        self.pasta_app = self.home_usuario / "Biblioteca"  # Ou a pasta que desejar
        
        # Se nenhum arquivo for passado, cria em ~/SuaAplicacao/Dados/Configuracoes.json
        if arquivo is None:
            self.arquivo = self.pasta_app / "Dados" / "Configuracoes.json"
        else:
            self.arquivo = Path(arquivo)

        self.dados_padrao = {
            "caminho_home": str(self.home_usuario),
            "caminho_biblioteca": str(self.pasta_app / "Biblioteca"),
            "tema": "Dark",
            "idioma": "pt-br",
            "animacoes": True,
            "categorias": [
                "Romance",
                "Matemática",
                "Programação",
                "História",
                "Filosofia",
                "Ciência",
                "Favoritos",
                "Outros"
            ]
        }
        

        self._garantir_arquivo()
        self.dados = self._carregar()

    def _garantir_arquivo(self):
        # Garante a existência da pasta pai do arquivo de configuração
        self.arquivo.parent.mkdir(parents=True, exist_ok=True)

        if self.arquivo.exists():
            return

        self.arquivo.write_text(
            json.dumps(self.dados_padrao, indent=4, ensure_ascii=False),
            encoding="utf-8"
        )

    def _carregar(self):
        try:
            with self.arquivo.open("r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            self._garantir_arquivo()
            return self.dados_padrao.copy()

    def salvar(self):
        with self.arquivo.open("w", encoding="utf-8") as f:
            json.dump(self.dados, f, indent=4, ensure_ascii=False)

    def obter(self, chave, padrao=None):
        return self.dados.get(chave, padrao)

    def obter_home(self) -> Path:
        # Retorna a Home salva no JSON ou a Home do sistema
        caminho = self.obter("caminho_home", str(self.home_usuario))
        return Path(caminho)

    def obter_pasta_biblioteca(self) -> Path:
        # Retorna a pasta da biblioteca configurada no JSON
        caminho_padrao = str(self.obter_home() / "SuaAplicacao" / "Biblioteca")
        caminho = self.obter("caminho_biblioteca", caminho_padrao)
        return Path(caminho)

    def obter_categorias(self) -> list:
        return self.obter("categorias", [])
