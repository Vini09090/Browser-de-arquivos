import json
from pathlib import Path


class Configuracoes:
    def __init__(self, arquivo="configuracoes.json"):
        self.arquivo = Path(arquivo)
        self.dados_padrao = {
            "tema": "Dark",
            "idioma": "pt-br",
            "animacoes": True,
            "categorias": [
                "Romance",
                "Matemática",
                "Programação",
                "História",
                "Filosofia",
                "Ciência"
            ]
        }

        self._garantir_arquivo()
        self.dados = self._carregar()

    def _garantir_arquivo(self):
        if not self.arquivo.exists():
            self.arquivo.write_text(
                json.dumps(
                    self.dados_padrao,
                    indent=4,
                    ensure_ascii=False
                ),
                encoding="utf-8"
            )

    def _carregar(self):
        try:
            with self.arquivo.open("r", encoding="utf-8") as arquivo:
                return json.load(arquivo)
        except (json.JSONDecodeError, OSError):
            self.arquivo.write_text(
                json.dumps(
                    self.dados_padrao,
                    indent=4,
                    ensure_ascii=False
                ),
                encoding="utf-8"
            )
            return self.dados_padrao.copy()

    def salvar(self):
        with self.arquivo.open("w", encoding="utf-8") as arquivo:
            json.dump(
                self.dados,
                arquivo,
                indent=4,
                ensure_ascii=False
            )

    def obter(self, chave, padrao=None):
        return self.dados.get(chave, padrao)

    def definir(self, chave, valor):
        self.dados[chave] = valor
        self.salvar()

    def obter_tema(self):
        return self.obter("tema", "Dark")

    def definir_tema(self, tema):
        self.definir("tema", tema)

    def obter_categorias(self):
        return self.obter("categorias", [])

    def adicionar_categoria(self, categoria):
        if categoria not in self.dados["categorias"]:
            self.dados["categorias"].append(categoria)
            self.salvar()

    def remover_categoria(self, categoria):
        if categoria in self.dados["categorias"]:
            self.dados["categorias"].remove(categoria)
            self.salvar()
