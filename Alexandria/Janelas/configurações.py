import customtkinter as ctk
from tema import definir_tema, alternar_tema, obter_tema

ctk.set_default_color_theme("blue")


class TelaConfiguracoes(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("Alexandria - Configurações")
        self.geometry("950x650")
        self.minsize(800, 550)

        definir_tema(obter_tema())

        self.sidebar_aberta = True
        self.sidebar_largura = 190

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(
            self,
            width=self.sidebar_largura,
            corner_radius=0,
            fg_color="#090909"
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        self.conteudo = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color="#111111"
        )
        self.conteudo.grid(row=0, column=1, sticky="nsew")
        self.conteudo.grid_rowconfigure(1, weight=1)
        self.conteudo.grid_columnconfigure(0, weight=1)

        self.criar_sidebar()
        self.criar_conteudo()
        self.mostrar_aparencia()

    def criar_sidebar(self):
        self.botao_menu = ctk.CTkButton(
            self.sidebar,
            text="☰",
            width=45,
            height=40,
            fg_color="transparent",
            hover_color="#292929",
            font=ctk.CTkFont(size=24),
            command=self.alternar_sidebar
        )
        self.botao_menu.pack(anchor="w", padx=12, pady=(15, 20))

        self.titulo_sidebar = ctk.CTkLabel(
            self.sidebar,
            text="CONFIGURAÇÕES",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#55EB19"
        )
        self.titulo_sidebar.pack(anchor="w", padx=18, pady=(0, 15))

        self.botao_aparencia = self.criar_item("◐", "Aparência", self.mostrar_aparencia)
        self.botao_informacoes = self.criar_item("ⓘ", "Informações", self.mostrar_informacoes)

        self.botao_voltar = ctk.CTkButton(
            self.sidebar,
            text="←  Voltar",
            anchor="w",
            height=42,
            fg_color="transparent",
            hover_color="#292929",
            font=ctk.CTkFont(size=14),
            command=self.destroy
        )
        self.botao_voltar.pack(side="bottom", fill="x", padx=10, pady=15)

    def criar_item(self, icone, texto, comando):
        botao = ctk.CTkButton(
            self.sidebar,
            text=f"{icone}   {texto}",
            anchor="w",
            height=44,
            corner_radius=7,
            fg_color="transparent",
            hover_color="#292929",
            font=ctk.CTkFont(size=14),
            command=comando
        )
        botao.pack(fill="x", padx=8, pady=3)
        return botao

    def criar_conteudo(self):
        self.barra_topo = ctk.CTkFrame(
            self.conteudo,
            height=70,
            corner_radius=0,
            fg_color="#161616"
        )
        self.barra_topo.grid(row=0, column=0, sticky="ew")
        self.barra_topo.grid_propagate(False)

        self.titulo = ctk.CTkLabel(
            self.barra_topo,
            text="Configurações",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color= "#55EB19"
        )
        self.titulo.pack(side="left", padx=25)

        self.area = ctk.CTkFrame(self.conteudo, fg_color="transparent")
        self.area.grid(row=1, column=0, sticky="nsew", padx=35, pady=30)
        self.area.grid_columnconfigure(0, weight=1)

    def limpar_area(self):
        for widget in self.area.winfo_children():
            widget.destroy()

    def mostrar_aparencia(self):
        self.limpar_area()
        self.selecionar_item(self.botao_aparencia)

        ctk.CTkLabel(
            self.area,
            text="Aparência",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color= "#55EB19"
        ).grid(row=0, column=0, sticky="w", pady=(5, 8))

        ctk.CTkLabel(
            self.area,
            text="Personalize a aparência do Alexandria.",
            font=ctk.CTkFont(size=14),
            text_color="#55EB19"
        ).grid(row=1, column=0, sticky="w", pady=(0, 25))

        cartao = ctk.CTkFrame(
            self.area,
            corner_radius=12,
            fg_color="#191919"
        )
        cartao.grid(row=2, column=0, sticky="ew", pady=8)
        cartao.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            cartao,
            text="Tema",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color= "#5EC336"
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(18, 3))

        self.label_tema = ctk.CTkLabel(
            cartao,
            text=self.texto_tema(),
            text_color="#5EC336"
        )
        self.label_tema.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 18))

        self.botao_tema = ctk.CTkButton(
            cartao,
            text=self.texto_botao_tema(),
            width=150,
            height=38,
            corner_radius=8,
            command=self.mudar_tema
        )
        self.botao_tema.grid(row=0, column=1, rowspan=2, padx=20)

    def mostrar_informacoes(self):
        self.limpar_area()
        self.selecionar_item(self.botao_informacoes)

        ctk.CTkLabel(
            self.area,
            text="Informações",
            font=ctk.CTkFont(size=28, weight="bold")
        ).grid(row=0, column=0, sticky="w", pady=(5, 8))

        ctk.CTkLabel(
            self.area,
            text="Sobre o Alexandria",
            font=ctk.CTkFont(size=15, weight="bold")
        ).grid(row=1, column=0, sticky="w", pady=(15, 4))

        ctk.CTkLabel(
            self.area,
            text="Sistema Neural de Biblioteca",
            font=ctk.CTkFont(size=14),
            text_color="#aaaaaa"
        ).grid(row=2, column=0, sticky="w")

        ctk.CTkLabel(
            self.area,
            text="Projeto desenvolvido para organização,\npesquisa e gerenciamento de livros.",
            justify="left",
            font=ctk.CTkFont(size=14),
            text_color="#888888"
        ).grid(row=3, column=0, sticky="w", pady=(20, 0))

        ctk.CTkLabel(
            self.area,
            text="Contato",
            font=ctk.CTkFont(size=19, weight="bold")
        ).grid(row=4, column=0, sticky="w", pady=(30, 4))

        ctk.CTkLabel(
            self.area,
            text="Palmeiravinicius04@gmail.com",
            font=ctk.CTkFont(size=17),
            text_color="#aaaaaa"
        ).grid(row=5, column=0, sticky="w")

        ctk.CTkLabel(
            self.area,
            text="GitHub: github.com/Brownser_arquivos",
            font=ctk.CTkFont(size=17),
            text_color="#aaaaaa"
        ).grid(row=6, column=0, sticky="w", pady=(4, 0))

    def selecionar_item(self, selecionado):
        for botao in (self.botao_aparencia, self.botao_informacoes):
            botao.configure(
                fg_color="#303030" if botao == selecionado else "transparent"
            )

    def texto_tema(self):
        return "Tema atual: Claro" if obter_tema() == "Light" else "Tema atual: Escuro"

    def texto_botao_tema(self):
        return "☀  Modo Claro" if obter_tema() == "Dark" else "☾  Modo Escuro"

    def mudar_tema(self):
        alternar_tema()
        self.label_tema.configure(text=self.texto_tema())
        self.botao_tema.configure(text=self.texto_botao_tema())

    def alternar_sidebar(self):
        if self.sidebar_aberta:
            self.sidebar.configure(width=65)
            self.titulo_sidebar.pack_forget()
            self.botao_aparencia.configure(text="◐")
            self.botao_informacoes.configure(text="ⓘ")
            self.botao_voltar.configure(text="←")
            self.sidebar_aberta = False
        else:
            self.sidebar.configure(width=self.sidebar_largura)
            self.titulo_sidebar.pack(
                anchor="w",
                padx=18,
                pady=(0, 15),
                before=self.botao_aparencia
            )
            self.botao_aparencia.configure(text="◐   Aparência")
            self.botao_informacoes.configure(text="ⓘ   Informações")
            self.botao_voltar.configure(text="←  Voltar")
            self.sidebar_aberta = True



