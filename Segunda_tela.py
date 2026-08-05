import customtkinter as ctk
import os 
from Brain import Livros

class TelaSecundaria(ctk.CTkToplevel):

    def __init__(self, master=None):
        super().__init__(master)

        self.geometry("550x550")
        self.title("Brain - Anotações")

        self.livros = Livros()

        titulo = ctk.CTkLabel(
            self,
            text="Sistema de Anotações",
            font=("Arial", 24)
        )

        titulo.pack(pady=20)

        self.nome_arquivo = ctk.CTkEntry(
            self,
            width=300,
            placeholder_text="Nome da Nota"
        )

        self.nome_arquivo.pack(pady=10)

        self.entrada_nota = ctk.CTkTextbox(
            self,
            width=420,
            height=220
        )

        self.entrada_nota.pack(pady=10)

        botao_salvar = ctk.CTkButton(
            self,
            text="Salvar Nota",
            command=self.salvar_nota
        )

        botao_salvar.pack(pady=10)

        botao_pdf = ctk.CTkButton(
            self,
            text="Converter para PDF",
            command=self.exportar_pdf
        )

        botao_pdf.pack(pady=10)

        self.label_status = ctk.CTkLabel(
            self,
            text=""
        )

        self.label_status.pack(pady=10)

    def salvar_nota(self):

        texto = self.entrada_nota.get("1.0", "end").strip()

        titulo = self.nome_arquivo.get()

        if titulo == "":
            titulo = "Minha_Nota"

        # NOVA PASTA
        pasta_notas = r"/home/vinicius/Biblioteca"

        # cria a pasta automaticamente
        os.makedirs(pasta_notas, exist_ok=True)

        # caminho completo
        nome_txt = os.path.join(
            pasta_notas,
            f"{titulo}.txt"
        )

        with open(nome_txt, "w", encoding="utf-8") as arquivo:

            arquivo.write(texto)

        self.label_status.configure(
            text=f"Nota salva em:\n{nome_txt}"
        )
    def exportar_pdf(self):

        titulo = self.nome_arquivo.get()

        if titulo == "":
            titulo = "Minha_Nota"

        pasta_notas = r"/home/vinicius/Biblioteca"

        arquivo_txt = os.path.join(
            pasta_notas,
            f"{titulo}.txt"
        )

        arquivo_pdf = os.path.join(
            pasta_notas,
            f"{titulo}.pdf"
        )

        if not os.path.exists(arquivo_txt):

            self.label_status.configure(
                text="Arquivo TXT não encontrado."
            )

            return

        sucesso = Livros.converter_txt_para_pdf(
            arquivo_txt,
            arquivo_pdf
        )

        if sucesso:

            self.label_status.configure(
                text=f"PDF criado em:\n{arquivo_pdf}"
            )

        else:

            self.label_status.configure(
                text="Erro ao gerar PDF."
            )
