import customtkinter as ctk
from PIL import Image
from app import App
import os

class Keys_login:
    """Gerencia os usuários através do arquivo usuarios.txt."""

    def __init__(self, arquivo_usuarios="usuarios.txt"):
        self.arquivo_usuarios = arquivo_usuarios

        # Cria o arquivo caso ele ainda não exista
        self.criar_arquivo()

    def criar_arquivo(self):
        """Cria o arquivo de usuários e adiciona o administrador inicial."""

        if not os.path.exists(self.arquivo_usuarios):
            with open(self.arquivo_usuarios, "w", encoding="utf-8") as arquivo:
                arquivo.write("admin:200604\n")

    def verificar_usuario(self, usuario):
        """
        Verifica se determinado usuário já existe.
        Retorna:
            True  -> usuário existe
            False -> usuário não existe"""

        usuario = usuario.strip()

        with open(self.arquivo_usuarios, "r", encoding="utf-8") as arquivo:

            for linha in arquivo:

                linha = linha.strip()

                if not linha:
                    continue

                try:
                    usuario_salvo, senha_salva = linha.split(":", 1)
                except ValueError:
                    continue

                usuario_salvo = usuario_salvo.strip()

                if usuario == usuario_salvo:
                    return True

        return False

    def verificar_login(self, usuario, senha):
        """
        Verifica usuário e senha no arquivo usuarios.txt.
        Retorna:
            True  -> login correto
            False -> login incorreto"""

        usuario = usuario.strip()

        with open(self.arquivo_usuarios, "r", encoding="utf-8") as arquivo:

            for linha in arquivo:

                linha = linha.strip()

                if not linha:
                    continue

                try:
                    usuario_salvo, senha_salva = linha.split(":", 1)
                except ValueError:
                    continue

                usuario_salvo = usuario_salvo.strip()
                senha_salva = senha_salva.strip()

                if usuario == usuario_salvo and senha == senha_salva:
                    return True

        return False

    def adicionar_conta(self, usuario, senha):
        """Adiciona um novo usuário ao arquivo."""

        usuario = usuario.strip()
        if not usuario or not senha:
            return False

        # Verifica se o usuário já existe
        if self.verificar_usuario(usuario):
            return False

        with open(self.arquivo_usuarios, "a", encoding="utf-8") as arquivo:
            arquivo.write(f"{usuario}:{senha}\n")

        return True

class TelaLogin(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.geometry("1200x800")
        self.title("Alexandria - Login")
        self.resizable(False, False)
        self.configure(fg_color="#0b0b0b")

        # Sistema responsável pelos usuários
        self.confirmar_usuario = Keys_login()

        # -----------------------------------------
        # IMAGEM DE FUNDO

        imagem = Image.open(
            "/home/vinicius/Alexandria1.0/Imagens/Fundo_mar.jpeg"
        )

        self.wallpaper = ctk.CTkImage(
            light_image=imagem,
            dark_image=imagem,
            size=(1200, 800)
        )

        self.fundo = ctk.CTkLabel(
            self,
            image=self.wallpaper,
            text=""
        )

        self.fundo.place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1
        )

        # -----------------------------------------
        # PAINEL

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

        # -----------------------------------------
        # TÍTULO

        self.titulo = ctk.CTkLabel(
            self.painel,
            text="ALEXANDRIA",
            font=("Arial", 42, "bold"),
            text_color="white"
        )
        self.titulo.pack(pady=(50, 10))

        # -----------------------------------------
        # SUBTÍTULO

        self.subtitulo = ctk.CTkLabel(
            self.painel,
            text="Acesse sua biblioteca digital",
            font=("Arial", 14),
            text_color="#bdbdbd"
        )
        self.subtitulo.pack(pady=(0, 45))

        # -----------------------------------------
        # USUÁRIO

        self.entrada_usuario = ctk.CTkEntry(
            self.painel,
            width=300,
            height=50,
            corner_radius=15,
            placeholder_text="Usuário",
            font=("Arial", 16)
        )

        self.entrada_usuario.pack(pady=13)

        # -----------------------------------------
        # SENHA
        
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

        # -----------------------------------------
        # BOTÃO LOGIN
        

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
        self.botao_login.pack(pady=(30, 15))

        # -----------------------------------------
        # BOTÃO CRIAR CONTA
        
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

        self.botao_criar_conta.pack(pady=(0, 20))

        # -----------------------------------------
        # STATUS
        self.label_status = ctk.CTkLabel(
            self.painel,
            text="",
            font=("Arial", 14)
        )

        self.label_status.pack()

        # -----------------------------------------
        # RODAPÉ

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
    # =====================================================
    # LOGIN

    def verificar_login(self):

        usuario = self.entrada_usuario.get().strip()
        senha = self.entrada_senha.get()

        if not usuario or not senha:

            self.label_status.configure(
                text="Preencha usuário e senha.",
                text_color="#ff4444"
            )

            return

        if self.confirmar_usuario.verificar_login(usuario, senha):

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

    # CRIAR CONTA
    def criar_conta(self):

        usuario = self.entrada_usuario.get().strip()
        senha = self.entrada_senha.get()

        if not usuario or not senha:

            self.label_status.configure(
                text="Preencha usuário e senha.",
                text_color="#ff4444"
            )

            return

        # Tenta adicionar a conta
        conta_criada = self.confirmar_usuario.adicionar_conta(
            usuario,
            senha
        )

        if conta_criada:

            self.label_status.configure(
                text="Conta criada com sucesso.",
                text_color="#00ff88"
            )

            # Limpa os campos
            self.entrada_usuario.delete(0, "end")
            self.entrada_senha.delete(0, "end")

        else:

            self.label_status.configure(
                text="Esse usuário já existe.",
                text_color="#ff4444"
            )

    def abrir_programa(self):

        self.withdraw()
        app = App(master=self)

        def ao_fechar():

            app.destroy()
            self.destroy()

        app.protocol(
            "WM_DELETE_WINDOW",
            ao_fechar
        )
        app.mainloop()

#iniciação 

if __name__ == "__main__":
    app = TelaLogin()
    app.mainloop()
