import os
import customtkinter as ctk
from Brain import Livros


PASTA_BIBLIOTECA = "/home/vinicius/Biblioteca"

class TelaSecundaria(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.geometry("600x580")
        self.title("Alexandria - Anotações")

        self.livros = Livros()

        ctk.CTkLabel(
            self,
            text="Sistema de Anotações",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        self.nome_arquivo = ctk.CTkEntry(
            self,
            width=320,
            height= 35,
            placeholder_text="Título da Nota"
        )
        self.nome_arquivo.pack(pady=10)

        self.entrada_nota = ctk.CTkTextbox(
            self,
            width=490,
            height=270
        )
        self.entrada_nota.pack(pady=10)
        self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botoes.pack(pady=10)

        ctk.CTkButton(
            self.frame_botoes,
            text="Salvar Nota",
            command=self.salvar_nota,
            fg_color="#004DD3"
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            self.frame_botoes,
            text="Converter para PDF",
            command=self.exportar_pdf,
            fg_color="#004DD3"
        ).pack(side="left", padx=10)

        self.label_status = ctk.CTkLabel(self, text="")
        self.label_status.pack(pady=10)

    def obter_titulo(self):
        titulo = self.nome_arquivo.get().strip()
        return titulo or "Minha_Nota"

    def salvar_nota(self):
        texto = self.entrada_nota.get("1.0", "end").strip()

        if not texto:
            self.label_status.configure(text="Digite algum conteúdo.")
            return

        os.makedirs(PASTA_BIBLIOTECA, exist_ok=True)

        titulo = self.obter_titulo()
        arquivo_txt = os.path.join(PASTA_BIBLIOTECA, f"{titulo}.txt")

        with open(arquivo_txt, "w", encoding="utf-8") as arquivo:
            arquivo.write(texto)

        self.label_status.configure(
            text=f"Nota salva em:\n{arquivo_txt}"
        )

    def exportar_pdf(self):
        os.makedirs(PASTA_BIBLIOTECA, exist_ok=True)

        titulo = self.obter_titulo()

        arquivo_txt = os.path.join(
            PASTA_BIBLIOTECA,
            f"{titulo}.txt"
        )

        arquivo_pdf = os.path.join(
            PASTA_BIBLIOTECA,
            f"{titulo}.pdf"
        )

        if not os.path.exists(arquivo_txt):
            self.label_status.configure(
                text="Salve a nota como TXT antes de gerar o PDF."
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



if __name__ == "__main__":
    app = TelaSecundaria()
    app.mainloop()
