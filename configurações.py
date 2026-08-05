import customtkinter as ctk
from PIL import Image



class TelaConfiguracoes(ctk.CTkToplevel):

    def __init__(self, master=None):
        super().__init__(master)

        self.master_app = master

        self.geometry("500x500")
        self.title("Brain - Configurações")

        titulo = ctk.CTkLabel(
            self,
            text="Configurações",
            font=("Arial", 24)
        )

        titulo.pack(pady=20)

        # ---------- FUNDOS ---------- #

        texto_fundo = ctk.CTkLabel(
            self,
            text="Escolha um Fundo"
        )

        texto_fundo.pack(pady=10)

        self.fundos = {

            "Original":
            "/home/vinicius/Imagens/wallpapers/Nova-foto.jpeg",

            "Deserto":
            "/home/vinicius/Imagens/wallpapers/deserto.jpg",

            "Espaço":
            "/home/vinicius/Imagens/wallpapers/espaco.jpg",

            "Floresta":
            "/home/vinicius/Imagens/wallpapers/floresta.jpg"
        }

        self.menu_fundos = ctk.CTkOptionMenu(
            self,
            values=list(self.fundos.keys()),
            command=self.trocar_fundo
        )

        self.menu_fundos.pack(pady=10)

        # ---------- CONTATO ---------- #

        separador = ctk.CTkLabel(
            self,
            text="────────────"
        )

        separador.pack(pady=20)

        titulo_contato = ctk.CTkLabel(
            self,
            text="Informações de Contato",
            font=("Arial", 20)
        )

        titulo_contato.pack(pady=10)

        contato = """
Email:
brainproject@email.com

GitHub:
github.com/brainproject

Telefone:
(77) 99999-9999
"""

        texto_contato = ctk.CTkLabel(
            self,
            text=contato,
            justify="left"
        )

        texto_contato.pack(pady=10)

    def trocar_fundo(self, escolha):

        caminho = self.fundos[escolha]

        nova_imagem = ctk.CTkImage(
            light_image=Image.open(caminho),
            dark_image=Image.open(caminho),
            size=(1200, 800)
        )

        self.master_app.imagem = nova_imagem

        self.master_app.background_label.configure(
            image=nova_imagem
        )
