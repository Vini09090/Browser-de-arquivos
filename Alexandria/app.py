import customtkinter as ctk
from Janelas.configurações import TelaConfiguracoes
from Janelas.Segunda_tela import TelaSecundaria
from Janelas.Tela_pesquisa import TelaPesquisa
from Janelas.rede_neural import TelaRedeNeural


class App(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.geometry("1200x800")
        self.title("Alexandria")
        self.configure(fg_color="#0b0b0b")
        self.minsize(900, 600)

        # CONFIGURAÇÃO DA SIDEBAR

        self.sidebar_open = True
        self.sidebar_width_open = 230
        self.sidebar_width_closed = 65
        self.animation_step = 15
        self.animating = False

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(
            self,
            width=self.sidebar_width_open,
            corner_radius=0,
            fg_color="#080909"
        )
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_propagate(False)

        # Área principal
        self.conteudo = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color="#0b0b0b"
        )
        self.conteudo.grid(row=0, column=1, sticky="nsew")

        self.conteudo.grid_rowconfigure(0, weight=1)
        self.conteudo.grid_columnconfigure(0, weight=1)

        self.menu_button = ctk.CTkButton(
            self.sidebar,
            text="☰",
            width=45,
            height=45,
            corner_radius=10,
            fg_color="transparent",
            hover_color="#242424",
            font=ctk.CTkFont(size=23),
            command=self.toggle_sidebar
        )
        self.menu_button.place(x=10, y=10)


        self.logo = ctk.CTkLabel(
            self.sidebar,
            text="ALEXANDRIA",
            font=("Arial", 21, "bold"),
            text_color="white"
        )
        self.logo.place(x=65, y=20)

        self.botoes_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )
        self.botoes_frame.place(
            x=8,
            y=85,
            relwidth=1,
            relheight=0.75
        )

        self.botao_pesquisa = self.criar_botao_sidebar(
            "📚", "Pesquisar Livros", self.pesquisar_livros
        )
        self.botao_pesquisa.pack(fill="x", pady=6)

        self.botao_anotacoes = self.criar_botao_sidebar(
            "📝", "Minhas Anotações", self.abrir_anotacoes
        )
        self.botao_anotacoes.pack(fill="x", pady=6)

        self.botao_rede = self.criar_botao_sidebar(
            "🧠", "Rede Neural", self.abrir_rede_neural
        )
        self.botao_rede.pack(fill="x", pady=6)

        self.botao_config = self.criar_botao_sidebar(
            "⚙", "Configurações", self.abrir_configuracoes
        )
        self.botao_config.pack(fill="x", pady=6)

        self.active_button = self.botao_pesquisa
        self.selecionar_botao(self.botao_pesquisa)

        # Tela Inicial
        self.criar_tela_inicial()


    def criar_botao_sidebar(self, icone, texto, comando):
        botao = ctk.CTkButton(
            self.botoes_frame,
            text=f"{icone}    {texto}",
            anchor="w",
            height=48,
            corner_radius=8,
            fg_color="transparent",
            hover_color="#20F109",
            font=ctk.CTkFont(size=15),
            command=comando,
            text_color= "#E8F716"
        )

        botao.icone = icone
        botao.texto = texto

        return botao


    def toggle_sidebar(self):
        if self.animating:
            return

        self.sidebar_open = not self.sidebar_open
        self.animating = True

        largura_atual = self.sidebar.winfo_width()

        if self.sidebar_open:
            largura_alvo = self.sidebar_width_open
            direcao = 1
        else:
            largura_alvo = self.sidebar_width_closed
            direcao = -1

        self.animar_sidebar(
            largura_atual,
            largura_alvo,
            direcao
        )

    def animar_sidebar(self, largura_atual, largura_alvo, direcao):
        diferenca = largura_alvo - largura_atual

        if abs(diferenca) <= self.animation_step:
            nova_largura = largura_alvo
        else:
            nova_largura = largura_atual + (
                direcao * self.animation_step
            )

        self.sidebar.configure(width=nova_largura)

        if nova_largura <= self.sidebar_width_closed + 5:
            self.sidebar_fechada()
        else:
            self.sidebar_aberta()

        if nova_largura == largura_alvo:
            self.animating = False
            return

        self.after(
            15,
            lambda: self.animar_sidebar(
                nova_largura,
                largura_alvo,
                direcao
            )
        )

    def sidebar_fechada(self):
        self.logo.place_forget()

        for botao in (
            self.botao_pesquisa,
            self.botao_anotacoes,
            self.botao_rede,
            self.botao_config
        ):
            botao.configure(
                text=botao.icone,
                anchor="center"
            )

    def sidebar_aberta(self):
        self.logo.place(x=65, y=20)

        for botao in (
            self.botao_pesquisa,
            self.botao_anotacoes,
            self.botao_rede,
            self.botao_config
        ):
            botao.configure(
                text=f"{botao.icone}    {botao.texto}",
                anchor="w"
            )

    def selecionar_botao(self, botao):
        for item in (
            self.botao_pesquisa,
            self.botao_anotacoes,
            self.botao_rede,
            self.botao_config
        ):
            item.configure(fg_color="transparent")

        botao.configure(fg_color="#303030")
        self.active_button = botao

    def criar_tela_inicial(self):
        container = ctk.CTkFrame(
            self.conteudo,
            fg_color="transparent"
        )
        container.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        centro = ctk.CTkFrame(
            container,
            fg_color="transparent"
        )
        centro.grid(
            row=0,
            column=0
        )

        ctk.CTkLabel(
            centro,
            text="ALEXANDRIA",
            font=("Arial", 46, "bold"),
            text_color="white"
        ).pack(pady=(0, 10))

        ctk.CTkLabel(
            centro,
            text="Sua biblioteca acadêmica pessoal",
            font=("Arial", 18),
            text_color="#9f9f9f"
        ).pack()

        ctk.CTkLabel(
            centro,
            text="Selecione uma opção no menu lateral",
            font=("Arial", 15),
            text_color="#666666"
        ).pack(pady=(25, 0))


    def pesquisar_livros(self):
        self.selecionar_botao(self.botao_pesquisa)
        TelaPesquisa(master=self)

    def abrir_anotacoes(self):
        self.selecionar_botao(self.botao_anotacoes)
        TelaSecundaria(master=self)

    def abrir_configuracoes(self):
        self.selecionar_botao(self.botao_config)
        TelaConfiguracoes(master=self)

    def abrir_rede_neural(self):
        self.selecionar_botao(self.botao_rede)
        TelaRedeNeural(master=self)


if __name__ == "__main__":
    app = App()
    app.mainloop()
