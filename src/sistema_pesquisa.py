import os
import webbrowser
from urllib.parse import quote_plus


class Pesquisa:
    EXTENSOES = (".pdf", ".epub", ".txt")

    def __init__(self, pasta_livros="/home/vinicius/Biblioteca"):
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

    def buscar_online(self, termo: str) -> list:
        termo_url = quote_plus(termo)

        return [
            {
                "titulo": f"🌐 OpenLibrary | {termo}",
                "url": f"https://openlibrary.org/search?q={termo_url}"
            },
            {
                "titulo": f"🌐 Google Books | {termo}",
                "url": f"https://books.google.com/books?q={termo_url}"
            },
            {
                "titulo": f"🌐 Projeto Gutenberg | {termo}",
                "url": f"https://www.gutenberg.org/ebooks/search/?query={termo_url}"
            },
            {
                "titulo": f"🏛 MEC Domínio Público | {termo}",
                "url": "http://www.dominiopublico.gov.br/pesquisa/"
                       "PesquisaObraForm.jsp"
            },
            {
                "titulo": f"📖 BibliON São Paulo | {termo}",
                "url": "https://biblion.odilo.us/"
            }
        ]

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
