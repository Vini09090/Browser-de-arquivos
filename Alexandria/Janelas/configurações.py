import customtkinter as ctk
from tkinter import filedialog

#task : criar uma função que faz o usuário escolher o diretório base.
class TelaConfiguracoes(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.geometry("650x500")
        self.title("Alexandria - Configurações")

        self.pasta_biblioteca = ""
        
        ctk.CTkLabel(
            self,
            text="Configurações",
            font=("Arial", 24, "bold")
        ).pack(pady=25)

        self.criar_secao("APARÊNCIA")

        ctk.CTkLabel(
            self,
            text="Tema atual: Escuro",
            text_color="#aaaaaa"
        ).pack(pady=5)

        self.criar_secao("BIBLIOTECA")

        self.label_pasta = ctk.CTkLabel(
            self,
            text=self.pasta_biblioteca,
            text_color="#aaaaaa"
        )
        self.label_pasta.pack(pady=(2,5))

        ctk.CTkLabel(
            self,
            text =self.pasta_biblioteca,
            text_color="#aaaaaa"
        ).pack(pady=5)

        self.criar_secao("INFORMAÇÕES")

        contato = (
            "Alexandria"
            "Sistema Neural de Biblioteca"
            "Email: Palmeiravinicius04@gmail.com"
            "GitHub: github.com/brainproject"
        )

        ctk.CTkLabel(
            self,
            text=contato,
            justify="left",
            text_color="#aaaaaa"
        ).pack(pady=10)


        btn = ctk.CTkButton(self, text="Escolher Pasta", command=self.selecionar_pasta)
        btn.pack(padx=20, pady=20)

    def criar_secao(self, titulo):
        ctk.CTkLabel(
            self,
            text=titulo,
            font=("Arial", 14, "bold"),
            text_color="#7C3AED"
        ).pack(pady=(25, 8))

    
    def selecionar_pasta(self):
        pasta = filedialog.askdirectory(title="Selecione a pasta")

        if pasta:
            self.pasta_biblioteca = pasta
            self.label_pasta.configure(text=pasta)
    