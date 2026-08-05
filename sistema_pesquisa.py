import os
import sys


class Sourch_Image: 
    def __init__(self):
        self.image_path = self.resource_path("assets/search.png")
    
    def resource_path(self, relative_path): #Localizando o caminho da imagem para o executável

        try:

            base_path = sys._MEIPASS

        except Exception:

            base_path = os.path.abspath(".")

        return os.path.join(
            base_path,
            relative_path
        )
        
class Pesquisa:
    def __init__(self):
        self.pesquisa = ""
        self.resultados = []
        self.url = ""
        
    def buscar_livros_locais(self, termo: str, pasta: str) -> list:

        resultados = []

        # extensões aceitas
        extensoes = [".pdf", ".epub", ".txt"]

        # verifica se a pasta existe
        if not os.path.exists(pasta):

            print("Pasta não encontrada:", pasta)

            return resultados

        for raiz, diretorios, arquivos in os.walk(pasta):

            for arquivo in arquivos:

                nome_arquivo = arquivo.lower()

                if termo.lower() in nome_arquivo:

                    for ext in extensoes:

                        if nome_arquivo.endswith(ext):

                            caminho = os.path.join(raiz, arquivo)

                            resultados.append({

                                "titulo": f"📚 LOCAL | {arquivo}",

                                "url": caminho
                            })

        return resultados
    

    # pesquisa principal que junta resultados locais e online
    def realizar_pesquisa(self, termo: str) -> list:
        self.pesquisa = termo
        if termo == "":
            return

        # MUDE PARA SUA PASTA REAL
        pasta_livros = "/home/vinicius/Documentos/livros-faculdade"

        # RESULTADOS LOCAIS
        resultados_locais = self.buscar_livros_locais(
            termo,
            pasta_livros
        )

        # RESULTADOS ONLINE
        resultados_online = [

    {
        "titulo": f"🌐 OpenLibrary | {termo}",
        "url": f"https://openlibrary.org/search?q={termo}"
    },

    {
        "titulo": f"🌐 Google Books | {termo}",
        "url": f"https://books.google.com/books?q={termo}"
    },

    {
        "titulo": f"🌐 Projeto Gutenberg | {termo}",
        "url": f"https://www.gutenberg.org/ebooks/search/?query={termo}"
    },

    # DOMÍNIO PÚBLICO MEC
    {
        "titulo": f"🏛 MEC Domínio Público | {termo}",

        "url":
        f"http://www.dominiopublico.gov.br/pesquisa/"
        f"PesquisaObraForm.jsp"
    },

    # DOMÍNIO PÚBLICO / BIBLIOTECA SP
    {
        "titulo": f"📖 BibliON São Paulo | {termo}",

        "url":
        f"https://biblion.odilo.us/"
    }

    #
]