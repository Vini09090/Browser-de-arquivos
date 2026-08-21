import customtkinter as ctk

from app import App


class Keys_login:
    """Gerencia usuários durante a execução do programa."""

    def __init__(self):
        self.usuarios = {}

    def nova_conta(self, usuario: str, senha: str) -> bool:
        usuario = usuario.strip()

        if not usuario or not senha:
            return False

        if usuario in self.usuarios:
            return False

        self.usuarios[usuario] = senha
        return True

    def login(self, usuario: str, senha: str) -> bool:
        return self.usuarios.get(usuario) == senha


class TelaLogin(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1200x800")
        self.title("Alexandria - Login")
        self.resizable(False, False)
        self.configure(fg_color="#0b0b0b")

        self.confirmar_usuario = Keys_login()

        self.painel = ctk.CTkFrame(
            self,
            width=500,
            height=520,
            corner_radius=32,
            fg_color="#1a1a1a",
            border_width=2,
            border_color="#2f2f2f"
        )
        self.painel.place(relx=0.5, rely=0.5, anchor="center")
        self.painel.pack_propagate(False)

        self.titulo = ctk.CTkLabel(
            self.painel,
            text="ALEXANDRIA",
            font=("Arial", 42, "bold"),
            text_color="white"
        )
        self.titulo.pack(pady=(50, 10))

        self.subtitulo = ctk.CTkLabel(
            self.painel,
            text="Acesse sua biblioteca digital",
            font=("Arial", 16),
            text_color="#bdbdbd"
        )
        self.subtitulo.pack(pady=(0, 45))

        self.entrada_usuario = ctk.CTkEntry(
            self.painel,
            width=300,
            height=50,
            corner_radius=15,
            placeholder_text="Usuário",
            font=("Arial", 16)
        )
        self.entrada_usuario.pack(pady=13)

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
            hover_color="#1a1a1a",
            command=self.criar_conta
        )
        self.botao_criar_conta.pack(pady=(0, 20))

        self.label_status = ctk.CTkLabel(
            self.painel,
            text="",
            font=("Arial", 14)
        )
        self.label_status.pack()

        self.footer = ctk.CTkLabel(
            self.painel,
            text="Alexandria © Biblioteca Neural",
            font=("Arial", 13),
            text_color="#707070"
        )
        self.footer.pack(side="bottom", pady=18)

    def verificar_login(self):
        usuario = self.entrada_usuario.get().strip()
        senha = self.entrada_senha.get()

        if self.confirmar_usuario.login(usuario, senha):
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
        usuario = self.entrada_usuario.get().strip()
        senha = self.entrada_senha.get()

        if not usuario or not senha:
            self.label_status.configure(
                text="Preencha usuário e senha.",
                text_color="#ff4444"
            )
            return

        if self.confirmar_usuario.nova_conta(usuario, senha):
            self.label_status.configure(
                text="Conta criada com sucesso.",
                text_color="#00ff88"
            )
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

        app.protocol("WM_DELETE_WINDOW", ao_fechar)
        app.mainloop()
