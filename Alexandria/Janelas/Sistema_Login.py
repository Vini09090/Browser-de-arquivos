import customtkinter as ctk
from app import App
from Renderizador import GerenciadorImagem
from pathlib import Path
from random import shuffle
from .Nova_conta import Criar_conta
from Dados.iniciar import perfil


BASE_DIR = Path(__file__).resolve().parent
PASTA_IMAGENS = BASE_DIR / "Imagens"

class Chave_acesso:
    def __init__(self, nome: str, senha: str):
        self.users = perfil(nome, senha)

    # Integração com o banco.
    def verificacao_login(self, usuario: str, senha: str) -> str:
        self.users = perfil(usuario, senha)

        if self.users.verificar() == True:
            return "usuário existe"
        else:
            return "não existe"


class TelaLogin(ctk.CTk):

    def __init__(self):

        super().__init__()


        self.geometry("1150x790")
        self.minsize(900, 650)
        self.title("Alexandria - Login")
        self.resizable(True, True)

        self.configure(
            fg_color="#0b0b0b"
        )


        self.imagens = GerenciadorImagem.listar_imagens(
            PASTA_IMAGENS
        )

        if not self.imagens:
            raise FileNotFoundError(
                f"Nenhuma imagem encontrada em:\n{PASTA_IMAGENS}"
            )

        self.caminho_fundo = self.imagens[0]

        self.gerenciador_imagem = GerenciadorImagem(
            self.caminho_fundo
        )


        self.fundo = ctk.CTkLabel(
            self,
            text=""
        )

        self.fundo.place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1
        )

        self.wallpaper = None

        self.bind(
            "<Configure>",
            self.atualizar_fundo
        )



        self.painel = ctk.CTkFrame(
            self,
            width=430,
            height=560,
            corner_radius=20,
            fg_color="#151519",
            border_width=1,
            border_color="#303038"
        )

        self.painel.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        self.painel.pack_propagate(False)


        self.titulo = ctk.CTkLabel(
            self.painel,
            text="Acessar conta",
            font=("Arial", 30, "bold"),
            text_color="#ffffff"
        )

        self.titulo.pack(
            pady=(45, 8)
        )



        self.subtitulo = ctk.CTkLabel(
            self.painel,
            text="Entre para acessar sua biblioteca digital",
            font=("Arial", 13),
            text_color="#9999A3"
        )

        self.subtitulo.pack(
            pady=(0, 38)
        )



        self.label_usuario = ctk.CTkLabel(
            self.painel,
            text="Nome de usuário",
            font=("Arial", 12, "bold"),
            text_color="#D0D0D5"
        )

        self.label_usuario.pack(
            anchor="w",
            padx=55,
            pady=(0, 8)
        )

        self.entrada_usuario = ctk.CTkEntry(
            self.painel,
            width=320,
            height=48,
            corner_radius=12,
            placeholder_text="Digite seu nome de usuário",
            placeholder_text_color="#707078",
            font=("Arial", 14),
            fg_color="#202024",
            border_color="#34343A",
            border_width=1
        )

        self.entrada_usuario.pack(
            pady=(0, 20)
        )


        self.label_senha = ctk.CTkLabel(
            self.painel,
            text="Senha",
            font=("Arial", 12, "bold"),
            text_color="#D0D0D5"
        )

        self.label_senha.pack(
            anchor="w",
            padx=55,
            pady=(0, 8)
        )

        self.entrada_senha = ctk.CTkEntry(
            self.painel,
            width=320,
            height=48,
            corner_radius=12,
            placeholder_text="Digite sua senha",
            placeholder_text_color="#707078",
            font=("Arial", 14),
            fg_color="#202024",
            border_color="#34343A",
            border_width=1,
            show="*"
        )

        self.entrada_senha.pack(
            pady=(0, 12)
        )

        self.mostrar_senha = ctk.BooleanVar(value=False)

        self.checkbox = ctk.CTkCheckBox(
            self.painel,
            text="Mostrar senha",
            variable=self.mostrar_senha,
            command=self.alternar_senha,
            font=("Arial", 12),
            text_color="#A0A0A8",
            fg_color="#326BE8",
            hover_color="#245AC7",
            border_color="#55555E"
        )

        self.checkbox.pack(
            anchor="w",
            padx=55,
            pady=(0, 25)
        )



        self.botao_login = ctk.CTkButton(
            self.painel,
            text="Entrar",
            width=320,
            height=50,
            corner_radius=12,
            font=("Arial", 16, "bold"),
            fg_color="#326BE8",
            hover_color="#245AC7",
            command=self.verificar_login
        )

        self.botao_login.pack(
            pady=(0, 15)
        )



        self.botao_criar_conta = ctk.CTkButton(
            self.painel,
            text="Criar uma nova conta",
            width=220,
            height=38,
            corner_radius=10,
            font=("Arial", 12),
            fg_color="transparent",
            border_width=1,
            border_color="#45454D",
            text_color="#AFAFB8",
            hover_color="#222228",
            command=self.criar_conta
        )

        self.botao_criar_conta.pack(
            pady=(0, 10)
        )


        self.label_status = ctk.CTkLabel(
            self.painel,
            text="",
            font=("Arial", 12)
        )

        self.label_status.pack(
            pady=(0, 5)
        )



        self.footer = ctk.CTkLabel(
            self.painel,
            text="Alexandria © Biblioteca Neural",
            font=("Arial", 10),
            text_color="#606068"
        )

        self.footer.pack(
            side="bottom",
            pady=15
        )


        self.after(
            100,
            self.atualizar_fundo
        )

    def alternar_senha(self):

        if self.mostrar_senha.get():
            self.entrada_senha.configure(show="")
        else:
            self.entrada_senha.configure(show="*")

    def atualizar_fundo(self, event=None):
        """
        Redimensiona a imagem usando SEMPRE a imagem original.

        Isso evita perda de qualidade causada por múltiplos
        redimensionamentos.
        """

        largura = self.winfo_width()
        altura = self.winfo_height()

        if largura <= 1 or altura <= 1:
            return

        imagem = self.gerenciador_imagem.preparar(
            largura,
            altura,
            brilho=0.80,
            saturacao=0.90
        )

        self.wallpaper = ctk.CTkImage(
            light_image=imagem,
            dark_image=imagem,
            size=(largura, altura)
        )

        self.fundo.configure(
            image=self.wallpaper
        )

        self.fundo.lower()

    def verificar_login(self):

        usuario = self.entrada_usuario.get().strip()
        senha = self.entrada_senha.get()

        if not usuario or not senha:
            self.label_status.configure(
                text="Preencha usuário e senha.",
                text_color="#ff4444"
            )
            return

        pessoa = perfil(usuario, senha)

        if pessoa.verificar():

            self.label_status.configure(
                text="Login realizado.",
                text_color="#00ff88"
            )

            self.abrir_programa()

        else:

            self.label_status.configure(
                text="Usuário ou senha incorretos.",
                text_color="#ff4444"
            )

    def criar_conta(self):
        self.janela_conta = Criar_conta(self)

    def abrir_programa(self):

        self.withdraw()

        app = App(
            master=self
        )

        def ao_fechar():

            app.destroy()
            self.destroy()

        app.protocol(
            "WM_DELETE_WINDOW",
            ao_fechar
        )

        app.mainloop()


if __name__ == "__main__":

    app = TelaLogin()
    app.mainloop()
