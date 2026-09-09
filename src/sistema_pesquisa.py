import os
import webbrowser
from urllib.parse import quote_plus
from Fontes import BuscadorDeLivros
import unicodedata

class Pesquisa:
    EXTENSOES = (".pdf", ".epub", ".txt")

    def __init__(self, pasta_livros= '/home/vinicius'):
        self.pasta_livros = pasta_livros
        self.pesquisa = ""
        self.resultados = []

    def normalizar_texto(self,texto: str) -> str:
        texto = texto.lower().strip()

        texto = unicodedata.normalize("NFD", texto)

        texto = "".join(
            caractere
            for caractere in texto
            if unicodedata.category(caractere) != "Mn"
        )

        texto = texto.replace(" ", "")

        return texto
    
    def buscar_livros_locais(self, termo: str) -> list:
        termo = self.normalizar_texto(termo)

        if not termo or not os.path.isdir(self.pasta_livros):
            return []

        resultados = []

        for raiz, _, arquivos in os.walk(self.pasta_livros):
            for arquivo in arquivos:

                nome_arquivo = self.normalizar_texto(arquivo)

                if (
                    termo in nome_arquivo
                    and arquivo.lower().endswith(self.EXTENSOES)
                ):
                    resultados.append({
                        "titulo": f"📚 LOCAL | {arquivo}",
                        "url": os.path.join(raiz, arquivo)
                    })

        return resultados

    
    def pesquisa_fonte(self, titulo: str) -> list:
        """
        Pesquisa nas fontes online e retorna somente obras realmente
        encontradas.
        """
        buscador = BuscadorDeLivros()
        fontes = buscador.buscar_em_todas(title=titulo, limit=5)

        resultados = []

        for fonte in fontes:
            if not isinstance(fonte, dict):
                continue

            nome_fonte = fonte.get("fonte", "Online")

            for resultado in fonte.get("resultados", []):
                if not isinstance(resultado, dict):
                    continue

                # Ignora fontes que não encontraram a obra.
                if not resultado.get("encontrado", True):
                    continue

                url = resultado.get("url")
                titulo_resultado = resultado.get("titulo")

                if not url or not titulo_resultado:
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
        # Não cria mais links genéricos de pesquisa.
        # Retorna apenas resultados realmente encontrados.
        return self.pesquisa_fonte(termo)

    
    def busca_inteligente(self, termo : str):
        resultados = self.pesquisa_fonte(titulo= termo)
        for resultado in resultados:
            if resultado == 0:
                return f"{resultado} | Nenhum resultado."
            else: 
                return f"{resultado} | Total de respostas."
        pass

        
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
        if os.path.exists(url):
            webbrowser.open(f"file://{os.path.abspath(url)}")
        else:
            webbrowser.open(url)
