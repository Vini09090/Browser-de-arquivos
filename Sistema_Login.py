import customtkinter as ctk
from PIL import Image
from sistema_pesquisa import Sourch_Image
from view import App

class sistema_Login:
    def __init__(self):
        self.usuario = []
        self.senha = []
        self.novo_perfil = {}

    def Nova_conta(self, usuario: str, senha: str) -> None:
        self.usuario.append(usuario)
        self.senha.append(senha)
        self.novo_perfil = {"usuario": self.usuario, "senha": self.senha}

    def Login(self, usuario: str, senha: str) -> bool:
        for u, s in zip(self.usuario, self.senha):
            if usuario == u and senha == s:
                return True
                
            else:
                return False
            


class TelaLogin(ctk.CTk):

    def __init__(self, app : None):
        super().__init__()

        self.App = app
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

        self.app = App()

        self.app.mainloop()

