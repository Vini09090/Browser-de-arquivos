import customtkinter as ctk


class TelaConfiguracoes(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.geometry("500x550")
        self.title("Alexandria - Configurações")

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

        ctk.CTkLabel(
            self,
            text="Pasta da biblioteca:",
            font=("Arial", 14, "bold")
        ).pack(pady=(5, 2))

        ctk.CTkLabel(
            self,
            text="/home/vinicius/Biblioteca",
            text_color="#aaaaaa"
        ).pack(pady=5)

        self.criar_secao("INFORMAÇÕES")

        contato = (
            "Alexandria"
            "Sistema Neural de Biblioteca"
            "Email: brainproject@email.com"
            "GitHub: github.com/brainproject"
        )

        ctk.CTkLabel(
            self,
            text=contato,
            justify="left",
            text_color="#aaaaaa"
        ).pack(pady=10)

    def criar_secao(self, titulo):
        ctk.CTkLabel(
            self,
            text=titulo,
            font=("Arial", 14, "bold"),
            text_color="#7C3AED"
        ).pack(pady=(25, 8))
