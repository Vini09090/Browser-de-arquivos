import customtkinter as ctk
from app import App
from Renderizador import GerenciadorImagem
from pathlib import Path
from random import shuffle
from .Nova_conta import Criar_conta
from Dados.iniciar import perfil

BASE_DIR = Path(__file__).resolve().parent
PASTA_IMAGENS = BASE_DIR / "Imagens"

EXTENSOES_IMAGEM = (
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".bmp"
)


def listar_imagens(diretorio):
    """
    Retorna somente arquivos que podem ser utilizados
    como imagens de fundo.
    """

    if not diretorio.exists():
        return []

    imagens = []

    for arquivo in diretorio.iterdir():

        if arquivo.is_file() and arquivo.suffix.lower() in EXTENSOES_IMAGEM:
            imagens.append(arquivo)

    shuffle(imagens)

    return imagens


class Chave_acesso:
    def __init__(self, nome: str , senha:str ):
        self.users = perfil(nome , senha)
        pass

    # Integração com o banco.
    def verificacao_login(self, usuario : str, senha :str) -> str: 
            self.users = perfil(usuario , senha)
            if self.users.verificar() == True:
                    return "usuário existe"
            else:
                    return "não existe"


class TelaLogin(ctk.CTk):

    def __init__(self):

        super().__init__()

        # ----------------------------------------------------
        # JANELA
        # ----------------------------------------------------

        self.geometry("1150x790")
        self.minsize(900, 650)

        self.title("Alexandria - Login")

        # Agora permitimos redimensionamento
        self.resizable(True, True)

        self.configure(
            fg_color="#0b0b0b"
        )

        # ----------------------------------------------------
        # IMAGENS
        # ----------------------------------------------------

        self.imagens = listar_imagens(
            PASTA_IMAGENS
        )

        if not self.imagens:

            raise FileNotFoundError(
                f"Nenhuma imagem encontrada em:\n{PASTA_IMAGENS}"
            )

        # Escolhe a primeira imagem aleatória
        self.caminho_fundo = self.imagens[0]

        # Cria o gerenciador usando a imagem ORIGINAL
        self.gerenciador_imagem = GerenciadorImagem(
            self.caminho_fundo
        )

        # ----------------------------------------------------
        # FUNDO
        # ----------------------------------------------------

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

        # Guarda a referência da imagem
        self.wallpaper = None

        # Atualiza o fundo quando a janela mudar
        self.bind(
            "<Configure>",
            self.atualizar_fundo
        )

        # ----------------------------------------------------
        # PAINEL
        # ----------------------------------------------------

        self.painel = ctk.CTkFrame(
            self,
            width=500,
            height=520,
            corner_radius=32,
            fg_color="#1a1a1a",
            border_width=2,
            border_color="#2f2f2f"
        )

        self.painel.place(
            relx=0.05,
            rely=0.5,
            anchor="w"
        )

        self.painel.pack_propagate(False)

        # ----------------------------------------------------
        # TÍTULO
        # ----------------------------------------------------

        self.titulo = ctk.CTkLabel(
            self.painel,
            text="ALEXANDRIA",
            font=("Arial", 42, "bold"),
            text_color="#ffffff"
        )

        self.titulo.pack(
            pady=(50, 10)
        )

        # ----------------------------------------------------
        # SUBTÍTULO
        # ----------------------------------------------------

        self.subtitulo = ctk.CTkLabel(
            self.painel,
            text="Acesse sua biblioteca digital",
            font=("Arial", 14),
            text_color="#bdbdbd"
        )

        self.subtitulo.pack(
            pady=(0, 45)
        )

        # ----------------------------------------------------
        # USUÁRIO
        # ----------------------------------------------------

        self.entrada_usuario = ctk.CTkEntry(
            self.painel,
            width=300,
            height=50,
            corner_radius=15,
            placeholder_text="Usuário",
            font=("Arial", 16)
        )

        self.entrada_usuario.pack(
            pady=13
        )

        # ----------------------------------------------------
        # SENHA
        # ----------------------------------------------------

        self.entrada_senha = ctk.CTkEntry(
            self.painel,
            width=300,
            height=50,
            corner_radius=15,
            placeholder_text="Senha",
            show="*",
            font=("Arial", 16)
        )

        self.entrada_senha.pack(
            pady=13
        )

        # ----------------------------------------------------
        # BOTÃO LOGIN
        # ----------------------------------------------------

        self.botao_login = ctk.CTkButton(
            self.painel,
            text="Entrar",
            width=300,
            height=50,
            corner_radius=15,
            font=("Arial", 18, "bold"),

            fg_color="#2563EB",
            hover_color="#1D4ED8",

            command=self.verificar_login
        )

        self.botao_login.pack(
            pady=(30, 15)
        )

        # ----------------------------------------------------
        # CRIAR CONTA
        # ----------------------------------------------------

        self.botao_criar_conta = ctk.CTkButton(
            self.painel,
            text="Criar Conta",
            width=220,
            height=40,
            corner_radius=20,

            fg_color="transparent",

            border_width=1,
            border_color="#7AF065",

            text_color="#39FF14",

            hover_color="#1a1a1a",

            command=self.criar_conta
        )

        self.botao_criar_conta.pack(
            pady=(0, 20)
        )

        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        self.label_status = ctk.CTkLabel(
            self.painel,
            text="",
            font=("Arial", 14)
        )

        self.label_status.pack()

        # ----------------------------------------------------
        # RODAPÉ
        # ----------------------------------------------------

        self.footer = ctk.CTkLabel(
            self.painel,
            text="Alexandria © Biblioteca Neural",
            font=("Arial", 13),
            text_color="#707070"
        )

        self.footer.pack(
            side="bottom",
            pady=18
        )

        # ----------------------------------------------------
        # PRIMEIRA RENDERIZAÇÃO
        # ----------------------------------------------------

        self.after(
            100,
            self.atualizar_fundo
        )


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

            # Ajustes visuais
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

        # Mantém o fundo atrás do painel
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
