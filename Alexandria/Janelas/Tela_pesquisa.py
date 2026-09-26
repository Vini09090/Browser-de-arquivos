import customtkinter as ctk
import threading
from Dados.sistema_pesquisa import Pesquisa
from Janelas.TelaExibição import Tela_exibição

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class TelaPesquisa(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.geometry("950x750")
        self.minsize(800, 550)
        self.title("Alexandria - Pesquisar Livros")

        self.pesquisa = Pesquisa()

        # -----------------------------
        # Configurações da Animação
        # -----------------------------
        self.sidebar_aberta = True
        self.sidebar_largura_aberta = 200
        self.sidebar_largura_fechada = 60
        self.animando = False
        self.passo_animacao = 12

        # Categoria e Dados
        self.categoria_selecionada = "📚 Todos"
        
        # Mapeamento com (emoji/ícone, nome_categoria)
        self.categorias = [
            ("📚", "Todos"),
            ("❤️", "Romance"),
            ("📐", "Matemática"),
            ("🔬", "Ciências"),
            ("💻", "Computação"),
            ("📖", "Literatura"),
            ("🏛️", "História"),
            ("🧠", "Filosofia"),
            ("🎨", "Artes"),
        ]

        # Layout Principal Grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # -----------------------------
        # 1. SIDEBAR
        # -----------------------------
        self.sidebar = ctk.CTkFrame(
            self,
            width=self.sidebar_largura_aberta,
            corner_radius=0,
            fg_color="#090909"
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        # -----------------------------
        # 2. CONTEÚDO PRINCIPAL
        # -----------------------------
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

    def criar_sidebar(self):
        # Botão do Menu para acionar a Animação
        self.botao_menu = ctk.CTkButton(
            self.sidebar,
            text="☰",
            width=42,
            height=40,
            fg_color="transparent",
            hover_color="#292929",
            font=ctk.CTkFont(size=22),
            command=self.alternar_sidebar
        )
        self.botao_menu.pack(anchor="w", padx=9, pady=(12, 10))

        # Título da Sidebar
        self.titulo_sidebar = ctk.CTkLabel(
            self.sidebar,
            text="CATEGORIAS",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#E8F716"
        )
        self.titulo_sidebar.pack(anchor="w", padx=15, pady=(0, 10))

        # Lista de Botões
        self.botoes_categorias = {}
        for icone, nome in self.categorias:
            texto_completo = f"{icone}  {nome}"
            
            btn = ctk.CTkButton(
                self.sidebar,
                text=texto_completo,
                anchor="w",
                height=40,
                corner_radius=7,
                fg_color="#303030" if texto_completo == self.categoria_selecionada else "transparent",
                hover_color="#292929",
                font=ctk.CTkFont(size=14),
                command=lambda c=texto_completo: self.selecionar_categoria(c)
            )
            btn.pack(fill="x", padx=6, pady=3)
            
            # Guardamos as referências de texto para a animação
            btn.icone = icone
            btn.nome = nome
            self.botoes_categorias[texto_completo] = btn

        # Botão Voltar
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
        self.botao_voltar.icone = "←"
        self.botao_voltar.nome = "Voltar"
        self.botao_voltar.pack(side="bottom", fill="x", padx=6, pady=15)

    # =========================================================
    # LÓGICA DE ANIMAÇÃO DA SIDEBAR
    # =========================================================
    def alternar_sidebar(self):
        if self.animando:
            return

        self.sidebar_aberta = not self.sidebar_aberta
        self.animando = True

        largura_atual = self.sidebar.winfo_width()
        
        if self.sidebar_aberta:
            largura_alvo = self.sidebar_largura_aberta
            direcao = 1
        else:
            largura_alvo = self.sidebar_largura_fechada
            direcao = -1

        self.animar_sidebar(largura_atual, largura_alvo, direcao)

    def animar_sidebar(self, largura_atual, largura_alvo, direcao):
        diferenca = largura_alvo - largura_atual

        if abs(diferenca) <= self.passo_animacao:
            nova_largura = largura_alvo
        else:
            nova_largura = largura_atual + (direcao * self.passo_animacao)

        self.sidebar.configure(width=nova_largura)

        # Alterna visualmente entre os modos compacto e expandido
        if nova_largura <= self.sidebar_largura_fechada + 10:
            self.modo_sidebar_compacto()
        else:
            self.modo_sidebar_expandido()

        if nova_largura == largura_alvo:
            self.animando = False
            return

        self.after(15, lambda: self.animar_sidebar(nova_largura, largura_alvo, direcao))

    def modo_sidebar_compacto(self):
        self.titulo_sidebar.pack_forget()

        for btn in self.botoes_categorias.values():
            btn.configure(text=btn.icone, anchor="center")

        self.botao_voltar.configure(text=self.botao_voltar.icone, anchor="center")

    def modo_sidebar_expandido(self):
        if not self.titulo_sidebar.winfo_ismapped():
            self.titulo_sidebar.pack(
                anchor="w",
                padx=15,
                pady=(0, 10),
                before=list(self.botoes_categorias.values())[0]
            )

        for btn in self.botoes_categorias.values():
            btn.configure(text=f"{btn.icone}  {btn.nome}", anchor="w")

        self.botao_voltar.configure(
            text=f"{self.botao_voltar.icone}  {self.botao_voltar.nome}",
            anchor="w"
        )

    # =========================================================
    # ÁREA DE CONTEÚDO E BUSCA
    # =========================================================
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
            text="Pesquisar Livros",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#E8F716"
        )
        self.titulo.pack(side="left", padx=25)

        self.area = ctk.CTkFrame(self.conteudo, fg_color="transparent")
        self.area.grid(row=1, column=0, sticky="nsew", padx=35, pady=40)
        self.area.grid_columnconfigure(0, weight=1)

        self.label_categoria_atual = ctk.CTkLabel(
            self.area,
            text=f"Categoria Selecionada: {self.categoria_selecionada}",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#aaaaaa"
        )
        self.label_categoria_atual.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 20))

        self.area_pesquisa = ctk.CTkFrame(self.area, fg_color="transparent")
        self.area_pesquisa.grid(row=1, column=0, sticky="ew")
        self.area_pesquisa.grid_columnconfigure(0, weight=1)

        self.entrada_pesquisa = ctk.CTkEntry(
            self.area_pesquisa,
            height=50,
            corner_radius=15,
            placeholder_text="Digite o nome do livro...",
            font=("Arial", 16)
        )
        self.entrada_pesquisa.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        self.botao_pesquisar = ctk.CTkButton(
            self.area_pesquisa,
            text="Pesquisar",
            width=135,
            height=50,
            corner_radius=15,
            command=self.realizar_pesquisa,
            fg_color="#003AA3",
            hover_color="#4AAE22",
            font=("Arial", 15, "bold"),
            text_color="#EBE5E5"
        )
        self.botao_pesquisar.grid(row=0, column=1)

        self.label_status = ctk.CTkLabel(
            self.area,
            text="",
            text_color="#aaaaaa",
            font=("Arial", 14)
        )
        self.label_status.grid(row=2, column=0, columnspan=2, sticky="w", pady=15)

        self.entrada_pesquisa.bind("<Return>", lambda event: self.realizar_pesquisa())

    def selecionar_categoria(self, categoria):
        self.categoria_selecionada = categoria
        self.label_categoria_atual.configure(
            text=f"Categoria Selecionada: {self.categoria_selecionada}"
        )

        for cat, btn in self.botoes_categorias.items():
            btn.configure(
                fg_color="#303030" if cat == categoria else "transparent"
            )

    def realizar_pesquisa(self):
        termo = self.entrada_pesquisa.get().strip()

        if not termo:
            self.label_status.configure(text="Digite algo para pesquisar.")
            return

        self.botao_pesquisar.configure(state="disabled", text="Pesquisando...")
        self.label_status.configure(text="Iniciando pesquisa...")

        self.janela_resultados = Tela_exibição(master=self)

        threading.Thread(
            target=self.executar_pesquisa,
            args=(termo,),
            daemon=True
        ).start()

    def executar_pesquisa(self, termo):
        resultados = self.pesquisa.realizar_pesquisa(termo)
        self.after(0, lambda: self.finalizar_pesquisa(resultados))

    def finalizar_pesquisa(self, resultados):
        self.botao_pesquisar.configure(state="normal", text="Pesquisar")

        if not resultados:
            self.label_status.configure(text="Nenhum resultado encontrado.")
            self.janela_resultados.exibir_resultados([])
            return

        self.label_status.configure(text=f"{len(resultados)} resultados encontrados.")
        self.janela_resultados.exibir_resultados(resultados)


if __name__ == "__main__":
    app = ctk.CTk()
    app.withdraw()
    tela = TelaPesquisa()
    tela.mainloop()
