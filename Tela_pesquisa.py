import customtkinter as ctk 
from TelaExibição import Tela_exibição
from Brain import Pesquisa

pesquisa = Pesquisa()


class TelaPesquisa(ctk.CTkToplevel):

    def __init__(self, master=None):
        super().__init__(master)

        self.geometry("600x350")
        self.title("Brain - Pesquisar Livros")

        titulo = ctk.CTkLabel(
            self,
            text="Pesquisar Livros",
            font=("Arial", 24)
        )

        titulo.pack(pady=20)

        self.entrada_pesquisa = ctk.CTkEntry(
            self,
            width=400,
            placeholder_text="Digite o nome do livro"
        )

        self.entrada_pesquisa.pack(pady=20)

        self.botao_pesquisar = ctk.CTkButton(
            self,
            text="Pesquisar",
            command=self.realizar_pesquisa
        )

        self.botao_pesquisar.pack(pady=15)

        # ----Pesquisa local ---------#
       

    def realizar_pesquisa(self):

        termo = self.entrada_pesquisa.get().strip()

        if termo == "":
            return

        # MUDE PARA SUA PASTA REAL
        pasta_livros = '/home/vinicius/Biblioteca'

        # RESULTADOS LOCAIS
        resultados_locais = pesquisa.buscar_livros_locais(
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
]

        # JUNTA OS DOIS
        resultados = []

        resultados.extend(resultados_locais)
        resultados.extend(resultados_online)

        # ABRE TELA DE RESULTADOS
        self.tela_resultados = Tela_exibição(
            master=self,
            resultados=resultados
        )