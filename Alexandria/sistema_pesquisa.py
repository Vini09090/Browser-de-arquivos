import os
import subprocess
import webbrowser
import unicodedata
from pathlib import Path 
from Dados.Fontes import BuscadorDeLivros

class Pesquisa:

    EXTENSOES = (".pdf", ".epub", ".txt", ".doc", ".docx")

    def __init__(self, pasta_livros="/home/vinicius", executavel_cpp=None):
        self.pasta_livros = pasta_livros

        if executavel_cpp is None:
            self.executavel_cpp = (
                Path(__file__).resolve().parent / "dados" / "buscador"
            )
        else:
            self.executavel_cpp = Path(executavel_cpp)

        self.pesquisa = ""
        self.resultados = []

    def normalizar_texto(self, texto: str) -> str:
        texto = str(texto).lower().strip()
        texto = unicodedata.normalize("NFD", texto)

        texto = "".join(
            c for c in texto
            if unicodedata.category(c) != "Mn"
        )

        return texto.replace(" ", "")

    def buscar_livros_locais_python(self, termo: str) -> list:
        termo_normalizado = self.normalizar_texto(termo)

        if not termo_normalizado or not os.path.isdir(self.pasta_livros):
            return []

        resultados = []

        for raiz, _, arquivos in os.walk(self.pasta_livros):
            for arquivo in arquivos:
                if not arquivo.lower().endswith(self.EXTENSOES):
                    continue

                nome_arquivo = os.path.splitext(arquivo)[0]
                nome_normalizado = self.normalizar_texto(nome_arquivo)

                if termo_normalizado in nome_normalizado:
                    resultados.append({
                        "titulo": f"📚 LOCAL | {nome_arquivo}",
                        "url": os.path.join(raiz, arquivo),
                        "fonte": "Local",
                        "similaridade": None
                    })

        return resultados

    def buscar_livros_locais(self, termo: str) -> list:
        termo = termo.strip()
        if not termo:
            return []

        try:
            processo = subprocess.run(
                [str(self.executavel_cpp), termo],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False
            )
        except (FileNotFoundError, PermissionError, OSError):
            return self.buscar_livros_locais_python(termo)

        if processo.returncode != 0:
            return self.buscar_livros_locais_python(termo)

        resultados = []

        for linha in processo.stdout.splitlines():
            partes = linha.strip().split("|", 2)

            if len(partes) != 3:
                continue

            try:
                similaridade = float(partes[0])
            except ValueError:
                continue

            titulo = partes[1].strip()
            caminho = partes[2].strip()

            if not caminho or not os.path.exists(caminho):
                continue

            resultados.append({
                "titulo": f"📚 LOCAL | {titulo}",
                "url": caminho,
                "fonte": "Local",
                "similaridade": similaridade
            })

        return resultados

    def _resultado_online_relevante(self, termo: str, titulo: str) -> bool:
        termo_original = unicodedata.normalize("NFD", str(termo).lower().strip())
        termo_original = "".join(
            c for c in termo_original
            if unicodedata.category(c) != "Mn"
        )

        termo_normalizado = self.normalizar_texto(termo)
        titulo_normalizado = self.normalizar_texto(titulo)

        if not termo_normalizado or not titulo_normalizado:
            return False

        if termo_normalizado in titulo_normalizado:
            return True

        palavras = [
            self.normalizar_texto(p)
            for p in termo_original.split()
            if len(p) >= 2
        ]

        if not palavras:
            return True

        encontradas = sum(
            1 for palavra in palavras
            if palavra and palavra in titulo_normalizado
        )

        return encontradas >= max(1, len(palavras) // 2)

    def pesquisa_fonte(self, titulo: str) -> list:
        try:
            fontes = BuscadorDeLivros().buscar_em_todas(
                title=titulo,
                limit=5
            )
        except Exception:
            return []

        resultados = []

        for fonte in fontes:
            if not isinstance(fonte, dict):
                continue

            nome_fonte = fonte.get("fonte", "Online")

            for resultado in fonte.get("resultados", []):
                if not isinstance(resultado, dict):
                    continue

                if not resultado.get("encontrado", True):
                    continue

                url = resultado.get("url")
                titulo_resultado = resultado.get("titulo")

                if not url or not titulo_resultado:
                    continue

                if not self._resultado_online_relevante(
                    titulo, titulo_resultado
                ):
                    continue

                resultados.append({
                    "titulo": f"🌐 {nome_fonte} | {titulo_resultado}",
                    "url": url,
                    "fonte": nome_fonte,
                    "autor": resultado.get("autor", []),
                    "ano": resultado.get("ano"),
                    "isbn": resultado.get("isbn", []),
                    "idioma": resultado.get("idioma", []),
                    "descricao": resultado.get("descricao"),
                    "download": resultado.get("download")
                })

        return resultados

    def buscar_online(self, termo: str) -> list:
        return self.pesquisa_fonte(termo)

    def busca_inteligente(self, termo: str):
        return len(self.realizar_pesquisa(termo))

    def realizar_pesquisa(self, termo: str) -> list:
        termo = termo.strip()

        if not termo:
            self.pesquisa = ""
            self.resultados = []
            return []

        self.pesquisa = termo

        resultados_locais = self.buscar_livros_locais(termo)
        resultados_online = self.buscar_online(termo)

        self.resultados = resultados_locais + resultados_online
        return self.resultados

    @staticmethod
    def abrir_resultado(url: str):
        if not url:
            return

        if os.path.exists(url):
            webbrowser.open(f"file://{os.path.abspath(url)}")
        else:
            webbrowser.open(url)
