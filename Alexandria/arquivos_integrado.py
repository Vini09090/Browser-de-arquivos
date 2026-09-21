import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from Brain import Livros
from pathlib import Path

class Janela_arquivos(ctk.CTkToplevel):
    """
    Janela responsável por selecionar um arquivo e movê-lo
    fisicamente para a Biblioteca do Brain.

    O parâmetro ao_adicionar permite avisar à janela principal
    que o arquivo foi adicionado com sucesso.
    """

    def __init__(
        self,
        master=None,
        ao_adicionar=None,
        pasta_biblioteca = Path.home() / "Biblioteca"
    ):
        super().__init__(master)

        self.master = master
        self.ao_adicionar = ao_adicionar
        self.pasta_biblioteca = pasta_biblioteca
        self.arquivo_selecionado = None

        self.livros = Livros()

        self.title("Adicionar arquivo")
        self.geometry("520x440")
        self.resizable(False, False)
        self.configure(fg_color="#0b0b0b")

        if master is not None:
            self.transient(master)

        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.fechar)

        self.criar_interface()

    def criar_interface(self):
        ctk.CTkLabel(
            self,
            text="＋  Adicionar arquivo",
            font=("Arial", 26, "bold"),
            text_color="white"
        ).pack(pady=(28, 5))

        ctk.CTkLabel(
            self,
            text="Adicione um arquivo à sua Biblioteca Neural",
            font=("Arial", 13),
            text_color="#898989"
        ).pack(pady=(0, 22))

        self.area = ctk.CTkFrame(
            self,
            fg_color="#111111",
            corner_radius=12,
            border_width=1,
            border_color="#242424"
        )
        self.area.pack(fill="x", padx=35)

        self.icone = ctk.CTkLabel(
            self.area,
            text="📄",
            font=("Arial", 35),
            text_color="#E8F716"
        )
        self.icone.pack(pady=(18, 5))

        self.nome_label = ctk.CTkLabel(
            self.area,
            text="Nenhum arquivo selecionado",
            font=("Arial", 14, "bold"),
            text_color="#898989"
        )
        self.nome_label.pack(pady=(0, 5))

        self.caminho_label = ctk.CTkLabel(
            self.area,
            text="Selecione um PDF, TXT ou EPUB",
            font=("Arial", 11),
            text_color="#666666",
            wraplength=420
        )
        self.caminho_label.pack(pady=(0, 20))

        self.botao_selecionar = ctk.CTkButton(
            self,
            text="Selecionar arquivo",
            width=250,
            height=40,
            corner_radius=8,
            fg_color="#202020",
            hover_color="#303030",
            text_color="white",
            font=("Arial", 13, "bold"),
            command=self.selecionar_arquivo
        )
        self.botao_selecionar.pack(pady=22)

        self.botao_adicionar = ctk.CTkButton(
            self,
            text="Adicionar à Biblioteca",
            width=250,
            height=42,
            corner_radius=8,
            fg_color="#E8F716",
            hover_color="#D4E500",
            text_color="black",
            font=("Arial", 13, "bold"),
            command=self.confirmar_adicao,
            state="disabled"
        )
        self.botao_adicionar.pack()

        self.status_label = ctk.CTkLabel(
            self,
            text="",
            font=("Arial", 11),
            text_color="#898989"
        )
        self.status_label.pack(pady=(12, 0))

    def selecionar_arquivo(self):
        caminho = filedialog.askopenfilename(
            parent=self,
            title="Selecione um arquivo",
            filetypes=[
                ("Arquivos da Biblioteca", "*.pdf *.txt *.epub"),
                ("Arquivos PDF", "*.pdf"),
                ("Arquivos TXT", "*.txt"),
                ("Arquivos EPUB", "*.epub"),
                ("Todos os arquivos", "*.*")
            ]
        )

        if not caminho:
            return

        self.arquivo_selecionado = os.path.abspath(caminho)

        nome = os.path.basename(self.arquivo_selecionado)

        self.icone.configure(text="📚")
        self.nome_label.configure(
            text=nome,
            text_color="white"
        )
        self.caminho_label.configure(
            text=self.arquivo_selecionado,
            text_color="#999999"
        )
        self.status_label.configure(
            text="Arquivo pronto para ser incorporado à rede neural",
            text_color="#E8F716"
        )
        self.botao_adicionar.configure(state="normal")

    def confirmar_adicao(self):
        if not self.arquivo_selecionado:
            return

        if not os.path.isfile(self.arquivo_selecionado):
            self.mostrar_erro("O arquivo selecionado não existe mais.")
            return

        nome = os.path.basename(self.arquivo_selecionado)
        pasta_origem = os.path.dirname(self.arquivo_selecionado)

        self.botao_adicionar.configure(state="disabled")
        self.botao_selecionar.configure(state="disabled")
        self.status_label.configure(
            text="Movendo arquivo para a Biblioteca...",
            text_color="#E8F716"
        )
        self.update_idletasks()

        sucesso = self.livros.mover_arquivos(
            destino=self.pasta_biblioteca,
            caminho_atual=pasta_origem,
            nome=nome
        )

        if not sucesso:
            self.botao_adicionar.configure(state="normal")
            self.botao_selecionar.configure(state="normal")
            self.mostrar_erro(
                "Não foi possível mover o arquivo. "
                "Verifique se ele já existe na Biblioteca."
            )
            return

        caminho_final = os.path.join(self.pasta_biblioteca, nome)

        self.status_label.configure(
            text="Arquivo adicionado com sucesso!",
            text_color="#55dd88"
        )

        # Atualiza a Rede Neural com o caminho real do arquivo.
        if callable(self.ao_adicionar):
            self.ao_adicionar(nome, caminho_final)

        self.after(500, self.fechar)

    def mostrar_erro(self, mensagem):
        self.status_label.configure(
            text=mensagem,
            text_color="#ff5555"
        )
        messagebox.showerror(
            "Erro ao adicionar arquivo",
            mensagem,
            parent=self
        )

    def fechar(self):
        try:
            self.grab_release()
        except ctk.TclError:
            pass

        self.destroy()


if __name__ == "__main__":
    app = ctk.CTk()
    app.withdraw()

    janela = Janela_arquivos(master=app)
    janela.mainloop()
