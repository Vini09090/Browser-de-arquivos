import customtkinter as ctk
from PIL import Image
from rede_neural import TelaRedeNeural
from configurações import TelaConfiguracoes
from Sistema_Login import sistema_Login
from Segunda_tela import TelaSecundaria
from Tela_pesquisa import TelaPesquisa
from sistema_pesquisa import Sourch_Image

class Container(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self._fg_color = "transparent"
        self.configure(fg_color=self._fg_color)

# ---------------- TELA LOGIN ---------------- #

class TelaLogin(ctk.CTk):

    def __init__(self):
        super().__init__()

        # ---------------- CONFIG ---------------- #

        self.geometry("1200x800")

        self.title("Alexandria - Login")

        self.resizable(False, False)

        self.confirmar_usuario = sistema_Login()
        self.localizar_imagem = Sourch_Image().resource_path("/home/vinicius/Imagens/wallpapers/Fundio_azul.jpeg")

        # ---------------- IMAGEM FUNDO ---------------- #

        self.imagem = ctk.CTkImage(

            light_image=Image.open(
                self.localizar_imagem
            ),

            dark_image=Image.open(
                self.localizar_imagem
            ),

            size=(1200, 800)
        )

        self.background = ctk.CTkLabel(
            self,
            image=self.imagem,
            text=""
        )

        self.background.place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1
        )

        # ---------------- OVERLAY ---------------- #

        self.overlay = ctk.CTkFrame(
            self,
            fg_color="#000000"
        )

        self.overlay.place(
            x=1400,
            y=0,
            relwidth=1,
            relheight=1
        )

        self.overlay.lower()
        self.background.lower()

        # ---------------- PAINEL LOGIN ---------------- #

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
            relx=0.5,
            rely=0.5,
            anchor="e"
        )

        self.painel.pack_propagate(False)

        
        # ---------------- TÍTULO ---------------- #

        self.titulo = ctk.CTkLabel(

            self.painel,

            text="ALEXANDRIA",

            font=("Arial", 42, "bold"),

            text_color="white"
        )

        self.titulo.pack(pady=(50, 10))

        # ---------------- SUBTÍTULO ---------------- #

        self.subtitulo = ctk.CTkLabel(

            self.painel,

            text="Acesse sua biblioteca digital",

            font=("Arial", 16),

            text_color="#bdbdbd"
        )

        self.subtitulo.pack(pady=(0, 45))

        # ---------------- ENTRADA USUÁRIO ---------------- #

        self.entrada_usuario = ctk.CTkEntry(

            self.painel,

            width=300,
            height=50,

            corner_radius=15,

            placeholder_text="Usuário",

            font=("Arial", 16)
        )

        self.entrada_usuario.pack(pady=13)

        # ---------------- ENTRADA SENHA ---------------- #

        self.entrada_senha = ctk.CTkEntry(

            self.painel,

            width=300,
            height=50,

            corner_radius=15,

            placeholder_text="Senha",

            show="*",

            font=("Arial", 16)
        )

        self.entrada_senha.pack(pady=13)

        # ---------------- BOTÃO LOGIN ---------------- #

        self.botao_login = ctk.CTkButton(

            self.painel,

            text="Entrar",

            width=300,
            height=50,

            corner_radius=15,

            font=("Arial", 18, "bold"),

            fg_color="#43EB25",

            hover_color="#1D4ED8",

            command=self.verificar_login
        )

        self.botao_login.pack(pady=(30, 15))

        self.botao_criar_conta = ctk.CTkButton(

            self.painel,

            text="Criar Conta",

            width=220,
            height=40,

            corner_radius=20,

            fg_color="transparent",

            border_width=1,

            border_color="#39FF14",

            text_color="#39FF14",

            hover_color="#1a1a1a"
        )

        self.botao_criar_conta.pack(
            pady=(0, 20)
        )

        # ---------------- STATUS ---------------- #

        self.label_status = ctk.CTkLabel(

            self.painel,

            text="",

            font=("Arial", 14),

            text_color="#ff5555"
        )

        self.label_status.pack()

        # ---------------- RODAPÉ ---------------- #

        self.footer = ctk.CTkLabel(

            self.painel,

            text="Alexandria © Biblioteca Neural",

            font=("Arial", 13),

            text_color="#707070"
        )

        self.footer.pack(side="bottom", pady=18)

    # ---------------- LOGIN ---------------- #
    

    def verificar_login(self):

        usuario = self.entrada_usuario.get()
        senha = self.entrada_senha.get()

        # LOGIN EXEMPLO
        if self.confirmar_usuario.Login(usuario, senha):

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
    
   

    
    def Criando_conta(self, usuário: str , senha: None):
            pass
    # ---------------- ABRIR APP ---------------- #

    def abrir_programa(self):

        self.destroy()

        app = App()

        app.mainloop()

# ---------------- APP PRINCIPAL ---------------- #
class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        # ------------------------------------------------
        # JANELA PRIMÁRIA
        # ------------------------------------------------

        self.geometry("1200x800")

        self.title("Alexandria")

        self.configure(
            fg_color="#0b0b0b"
        )

        # ------------------------------------------------
        # FRAME CENTRAL
        # ------------------------------------------------

        self.bloco_das_ops = ctk.CTkFrame(

            self,

            width=950,
            height=650,

            corner_radius=30,

            fg_color="#161616",

            border_width=2,

            border_color="#2d2d2d"
        )

        self.bloco_das_ops.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        self.bloco_das_ops.pack_propagate(False)

        # ------------------------------------------------
        # CONTAINER
        # ------------------------------------------------

        self.container = ctk.CTkFrame(

            self.bloco_das_ops,

            fg_color="transparent"
        )

        self.container.place(
            relx=0.5,
            rely=0.45,
            anchor="center"
        )

        # ------------------------------------------------
        # TÍTULO
        # ------------------------------------------------

        self.titulo = ctk.CTkLabel(

            self.container,

            text="ALEXANDRIA",

            font=("Arial", 46, "bold"),

            text_color="white"
        )

        self.titulo.pack(
            pady=(0, 10)
        )

        # ------------------------------------------------
        # SUBTÍTULO
        # ------------------------------------------------

        self.subtitulo = ctk.CTkLabel(

            self.container,

            text="Sua biblioteca acadêmica pessoal",

            font=("Arial", 18),

            text_color="#9f9f9f"
        )

        self.subtitulo.pack(
            pady=(0, 45)
        )

        # ------------------------------------------------
        # BOTÃO PESQUISAR
        # ------------------------------------------------

        self.botao_pesquisa = ctk.CTkButton(

            self.container,

            text="📚 Pesquisar Livros",

            width=320,
            height=55,

            corner_radius=18,

            font=("Arial", 18, "bold"),

            fg_color="#2563EB",

            hover_color="#1D4ED8",

            command=self.pesquisar_livros
        )

        self.botao_pesquisa.pack(
            pady=12
        )

        # ------------------------------------------------
        # BOTÃO NOTAS
        # ------------------------------------------------

        self.botao_notas = ctk.CTkButton(

            self.container,

            text="📝 Minhas Anotações",

            width=320,
            height=55,

            corner_radius=18,

            font=("Arial", 18, "bold"),

            fg_color="#059669",

            hover_color="#047857",

            command=self.abrir_tela
        )

        self.botao_notas.pack(
            pady=12
        )

        # ------------------------------------------------
        # BOTÃO REDE NEURAL
        # ------------------------------------------------

        self.botao_rede = ctk.CTkButton(

            self.container,

            text="🧠 Rede Neural",

            width=320,
            height=55,

            corner_radius=18,

            font=("Arial", 18, "bold"),

            fg_color="#EA580C",

            hover_color="#C2410C",

            command=self.abrir_rede_neural
        )

        self.botao_rede.pack(
            pady=12
        )

        # ------------------------------------------------
        # BOTÃO CONFIGURAÇÕES
        # ------------------------------------------------

        self.botao_config = ctk.CTkButton(

            self.container,

            text="⚙ Configurações",

            width=320,
            height=55,

            corner_radius=18,

            font=("Arial", 18, "bold"),

            fg_color="#7C3AED",

            hover_color="#6D28D9",

            command=self.abrir_configuracoes
        )

        self.botao_config.pack(
            pady=12
        )

        # ------------------------------------------------
        # RODAPÉ
        # ------------------------------------------------

        self.footer = ctk.CTkLabel(

            self.bloco_das_ops,

            text="Alexandria © Sistema Neural de Biblioteca",

            font=("Arial", 14),

            text_color="#666666"
        )

        self.footer.place(
            relx=0.5,
            rely=0.93,
            anchor="center"
        )

    # ====================================================
    # ABRIR NOTAS
    # ====================================================

    def abrir_tela(self):

        self.tela_notas = TelaSecundaria(
            master=self
        )

    # ====================================================
    # PESQUISA
    # ====================================================

    def pesquisar_livros(self):

        self.tela_pesquisa = TelaPesquisa(
            master=self
        )

    # ====================================================
    # CONFIGURAÇÕES
    # ====================================================

    def abrir_configuracoes(self):

        self.tela_config = TelaConfiguracoes(
            master=self
        )

    # ====================================================
    # REDE NEURAL - CONSTELAÇÃO DOS LIVROS DA BIBLIOTECA
    # ====================================================

    def abrir_rede_neural(self):

        self.tela_rede = TelaRedeNeural(
            master=self
        )
# ---------------- EXECUÇÃO ---------------- #

login = TelaLogin()
login.mainloop()