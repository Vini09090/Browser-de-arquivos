import customtkinter as ctk
import colorsys
import math
import os
import random
import webbrowser
from Janelas.arquivos_integrado import Janela_arquivos
from pathlib import Path
from Janelas.Renderizador import GerenciadorImagem

# Recursos incluídos na raiz do projeto/pacote.
PASTA_ICONS = Path(__file__).resolve().parent.parent / "icons"

# Nome da categoria usada para arquivos soltos na raiz da biblioteca.
CATEGORIA_PADRAO = "Geral"

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class TelaRedeNeuralCategorias(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.geometry("1200x800")
        self.title("Alexandria - Rede Neural por Categorias")
        self.configure(fg_color="#0b0b0b")
        self.minsize(950, 650)

        self.header = ctk.CTkFrame(
            self,
            fg_color="#080909",
            corner_radius=0,
            height=75
        )
        self.header.pack(fill="x")
        self.header.pack_propagate(False)

        ctk.CTkLabel(
            self.header,
            text="🧠",
            font=ctk.CTkFont(size=28),
            text_color="#E8F716"
        ).pack(side="left", padx=(25, 8))

        ctk.CTkLabel(
            self.header,
            text="REDE NEURAL",
            font=("Arial", 24, "bold"),
            text_color="white"
        ).pack(side="left")

        # Botão para adicionar um novo arquivo
        ctk.CTkButton(
            self.header,
            text="",
            width=160,
            height=38,
            corner_radius=10,
            fg_color="#202020",
            hover_color="#303030",
            text_color="white",
            font=("Arial", 13, "bold"),
            command=self.adicionar_arquivo,
            image=GerenciadorImagem.Criar_icone(PASTA_ICONS / "add.png")
        ).pack(side="right", padx=(10, 20))

        # Botão voltar
        ctk.CTkButton(
            self.header,
            text="",
            width=90,
            height=38,
            corner_radius=8,
            fg_color="transparent",
            hover_color="#242424",
            text_color="#E8F716",
            command=self.destroy,
            image=GerenciadorImagem.Criar_icone(PASTA_ICONS / "voltar.png")
        ).pack(side="right", padx=10)

        self.conteudo = ctk.CTkFrame(
            self,
            fg_color="#0b0b0b",
            corner_radius=0
        )
        self.conteudo.pack(fill="both", expand=True, padx=25, pady=18)

        ctk.CTkLabel(
            self.conteudo,
            text="Sua Rede Neural",
            font=("Arial", 30, "bold"),
            text_color="white"
        ).pack(pady=(8, 4))

        ctk.CTkLabel(
            self.conteudo,
            text="Cada ponto é um livro; cada cor é uma categoria da sua biblioteca",
            font=("Arial", 15),
            text_color="#9f9f9f"
        ).pack(pady=(0, 16))

        self.rede_frame = ctk.CTkFrame(
            self.conteudo,
            fg_color="#111111",
            corner_radius=12,
            border_width=1,
            border_color="#242424"
        )
        self.rede_frame.pack(fill="both", expand=True, padx=15, pady=5)

        self.rede_frame.grid_rowconfigure(0, weight=1)
        self.rede_frame.grid_columnconfigure(0, weight=1)

        self.constelacao = ConstelacaoCategoriasCanvas(
            self.rede_frame,
            pasta_livros=Path.home() / "Biblioteca",
            width=1100,
            height=620
        )
        self.constelacao.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=8,
            pady=8
        )

        self.info_frame = ctk.CTkFrame(
            self.conteudo,
            fg_color="#111111",
            corner_radius=10,
            height=62
        )
        self.info_frame.pack(fill="x", padx=15, pady=(7, 0))
        self.info_frame.pack_propagate(False)

        # Número de arquivos em destaque
        self.contador_label = ctk.CTkLabel(
            self.info_frame,
            text="",
            font=("Arial", 18, "bold"),
            text_color="#E8F716"
        )
        self.contador_label.pack(side="left", padx=18)

        # Legenda com uma entrada colorida por categoria
        self.legenda_frame = ctk.CTkFrame(self.info_frame, fg_color="transparent")
        self.legenda_frame.pack(side="left", padx=(5, 15))

        self.atualizar_contador()

    def atualizar_contador(self):
        quantidade = len(self.constelacao.estrelas)

        self.contador_label.configure(
            text=f"📚  {quantidade} arquivos conectados"
        )

        # Reconstrói a legenda
        for widget in self.legenda_frame.winfo_children():
            widget.destroy()

        for categoria in self.constelacao.categorias.values():
            ctk.CTkLabel(
                self.legenda_frame,
                text=f"● {categoria['nome']} ({len(categoria['estrelas'])})",
                font=("Arial", 13, "bold"),
                text_color=categoria["cor"]
            ).pack(side="left", padx=8)

    def adicionar_arquivo(self):
        app = Janela_arquivos(self)
        app.mainloop()
        # Recarrega a rede caso novos arquivos tenham sido adicionados
        self.constelacao.recarregar()
        self.atualizar_contador()


class ConstelacaoCategoriasCanvas(ctk.CTkCanvas):
    """
    Cada subpasta direta de `pasta_livros` é uma categoria.
    Arquivos soltos na raiz entram na categoria "Geral".
    Cada categoria forma uma constelação própria (cor e posição próprias):
    as estrelas só se ligam a estrelas da mesma categoria.
    """

    def __init__(self, master, pasta_livros, width=900, height=500):
        super().__init__(
            master,
            width=width,
            height=height,
            bg="#111111",
            highlightthickness=0
        )

        self.width = width
        self.height = height
        self.pasta_livros = pasta_livros
        self.estrelas = []
        self.categorias = {}  # nome -> dict com cor, centro, estrelas, texto_id

        self.carregar_livros()
        self.bind("<Configure>", self.ao_redimensionar)
        self.animar()

    # ------------------------------------------------------------------
    # Carregamento e organização por categoria
    # ------------------------------------------------------------------
    def carregar_livros(self):
        if not os.path.isdir(self.pasta_livros):
            return

        encontrados = []  # (categoria, nome, caminho)

        for raiz, _, arquivos in os.walk(self.pasta_livros):
            relativo = Path(raiz).relative_to(self.pasta_livros)
            categoria = relativo.parts[0] if relativo.parts else CATEGORIA_PADRAO

            for arquivo in arquivos:
                if arquivo.lower().endswith((".pdf", ".txt", ".epub")):
                    encontrados.append(
                        (categoria, arquivo, os.path.join(raiz, arquivo))
                    )

        # Cria as categorias (ordenadas) e atribui uma cor a cada uma
        contagem = {}
        for categoria, _, _ in encontrados:
            contagem[categoria] = contagem.get(categoria, 0) + 1

        nomes = sorted(contagem)
        for indice, nome in enumerate(nomes):
            self.criar_categoria(
                nome,
                self.gerar_cor(indice, len(nomes)),
                contagem[nome]
            )

        self.calcular_centros()

        for categoria, nome, caminho in encontrados:
            self.criar_estrela(categoria, nome, caminho)

    def gerar_cor(self, indice, total):
        # Distribui os tons igualmente no círculo de cores,
        # assim qualquer número de categorias recebe cores diferentes.
        matiz = indice / max(total, 1)
        r, g, b = colorsys.hsv_to_rgb(matiz, 0.65, 1.0)
        return "#{:02x}{:02x}{:02x}".format(int(r * 255), int(g * 255), int(b * 255))

    def criar_categoria(self, nome, cor, quantidade=1):
        texto_id = self.create_text(
            0, 0,
            text=nome.upper(),
            fill=cor,
            font=("Arial", 12, "bold")
        )

        self.categorias[nome] = {
            "nome": nome,
            "cor": cor,
            "cx": 0,
            "cy": 0,
            "raio": 100,
            "quantidade": quantidade,
            "texto_id": texto_id,
            "estrelas": []
        }

    def calcular_centros(self):
        """
        Distribui as constelações em uma grade que se adapta ao tamanho do canvas.
        Cada categoria ocupa uma célula, então nada se sobrepõe nem sai da tela,
        seja em janela pequena ou em tela cheia.
        """
        total = len(self.categorias)
        if total == 0:
            return

        colunas = math.ceil(math.sqrt(total * self.width / max(self.height, 1)))
        colunas = max(1, min(colunas, total))
        linhas = math.ceil(total / colunas)

        largura_celula = self.width / colunas
        altura_celula = self.height / linhas
        raio_max = max(min(largura_celula, altura_celula) * 0.36, 40)
        maior = max(c["quantidade"] for c in self.categorias.values()) or 1

        for indice, categoria in enumerate(self.categorias.values()):
            linha = indice // colunas
            coluna = indice % colunas

            # A última linha (incompleta) fica centralizada
            na_linha = min(colunas, total - linha * colunas)
            margem_x = (self.width - na_linha * largura_celula) / 2

            cx = margem_x + (coluna + 0.5) * largura_celula
            cy = (linha + 0.5) * altura_celula + 10

            # Categorias com mais livros ganham uma área um pouco maior
            fator = 0.55 + 0.45 * math.sqrt(categoria["quantidade"] / maior)
            raio = raio_max * fator

            # Move as estrelas existentes junto com a constelação
            antigo_cx = categoria["cx"]
            antigo_cy = categoria["cy"]
            antigo_raio = categoria["raio"]
            escala = raio / antigo_raio if antigo_raio else 1

            for estrela in categoria["estrelas"]:
                estrela["x"] = cx + (estrela["x"] - antigo_cx) * escala
                estrela["y"] = cy + (estrela["y"] - antigo_cy) * escala

            categoria["cx"] = cx
            categoria["cy"] = cy
            categoria["raio"] = raio
            self.coords(categoria["texto_id"], cx, cy - raio - 14)

    def ao_redimensionar(self, event):
        if event.width < 100 or event.height < 100:
            return

        self.width = event.width
        self.height = event.height
        self.calcular_centros()

    def recarregar(self):
        self.delete("all")
        self.estrelas.clear()
        self.categorias.clear()
        self.carregar_livros()

    # ------------------------------------------------------------------
    # Estrelas
    # ------------------------------------------------------------------
    def criar_estrela(self, nome_categoria, nome, caminho):
        categoria = self.categorias[nome_categoria]
        cor = categoria["cor"]

        # Nasce dentro da área da própria constelação
        angulo = random.uniform(0, 2 * math.pi)
        distancia = random.uniform(0, categoria["raio"] * 0.8)
        x = categoria["cx"] + distancia * math.cos(angulo)
        y = categoria["cy"] + distancia * math.sin(angulo)

        tamanho = random.randint(3, 5)
        vx = random.uniform(-0.3, 0.3)
        vy = random.uniform(-0.3, 0.3)

        estrela_id = self.create_oval(
            x - tamanho,
            y - tamanho,
            x + tamanho,
            y + tamanho,
            fill=cor,
            outline=""
        )

        texto_id = self.create_text(
            x,
            y + 18,
            text=nome[:25],
            fill="white",
            font=("Arial", 10),
            state="hidden"
        )

        estrela = {
            "x": x,
            "y": y,
            "vx": vx,
            "vy": vy,
            "tamanho": tamanho,
            "nome": nome,
            "categoria": nome_categoria,
            "cor": cor,
            "caminho": caminho,
            "estrela_id": estrela_id,
            "texto_id": texto_id
        }

        self.tag_bind(
            estrela_id,
            "<Button-1>",
            lambda event, path=caminho: self.abrir_arquivo(path)
        )

        self.tag_bind(
            texto_id,
            "<Button-1>",
            lambda event, path=caminho: self.abrir_arquivo(path)
        )

        for item in (estrela_id, texto_id):
            self.tag_bind(
                item,
                "<Enter>",
                lambda event, e=estrela: self.mostrar_nome(e)
            )
            self.tag_bind(
                item,
                "<Leave>",
                lambda event, e=estrela: self.esconder_nome(e)
            )

        self.estrelas.append(estrela)
        categoria["estrelas"].append(estrela)

    def mostrar_nome(self, estrela):
        self.itemconfigure(estrela["texto_id"], state="normal")
        self.itemconfigure(estrela["estrela_id"], outline="white", width=1)
        self.tag_raise(estrela["texto_id"])
        self.config(cursor="hand2")

    def esconder_nome(self, estrela):
        self.itemconfigure(estrela["texto_id"], state="hidden")
        self.itemconfigure(estrela["estrela_id"], outline="")
        self.config(cursor="")

    def abrir_arquivo(self, caminho):
        if os.path.exists(caminho):
            webbrowser.open(f"file://{os.path.abspath(caminho)}")

    # ------------------------------------------------------------------
    # Linhas: só ligam estrelas da mesma categoria
    # ------------------------------------------------------------------
    def desenhar_linhas(self):
        self.delete("linha")

        for categoria in self.categorias.values():
            membros = categoria["estrelas"]
            limite = categoria["raio"] * 0.9

            for i, estrela1 in enumerate(membros):
                for estrela2 in membros[i + 1:]:
                    distancia = math.hypot(
                        estrela1["x"] - estrela2["x"],
                        estrela1["y"] - estrela2["y"]
                    )

                    if distancia < limite:
                        self.create_line(
                            estrela1["x"],
                            estrela1["y"],
                            estrela2["x"],
                            estrela2["y"],
                            fill=categoria["cor"],
                            width=1,
                            tags="linha"
                        )

        # Mantém as linhas atrás das estrelas e dos textos
        self.tag_lower("linha")

    # ------------------------------------------------------------------
    # Animação
    # ------------------------------------------------------------------
    def animar(self):
        for estrela in self.estrelas:
            categoria = self.categorias[estrela["categoria"]]

            estrela["x"] += estrela["vx"]
            estrela["y"] += estrela["vy"]

            # Mantém a estrela dentro da região da sua constelação:
            # ao sair do raio, é puxada de volta ao centro da categoria.
            dx = categoria["cx"] - estrela["x"]
            dy = categoria["cy"] - estrela["y"]
            distancia = math.hypot(dx, dy)

            if distancia > categoria["raio"]:
                estrela["vx"] += dx / distancia * 0.08
                estrela["vy"] += dy / distancia * 0.08

            # Limita a velocidade para o movimento continuar suave
            velocidade = math.hypot(estrela["vx"], estrela["vy"])
            if velocidade > 0.45:
                estrela["vx"] *= 0.45 / velocidade
                estrela["vy"] *= 0.45 / velocidade

            # Pequena variação aleatória mantém a rede "viva"
            estrela["vx"] += random.uniform(-0.02, 0.02)
            estrela["vy"] += random.uniform(-0.02, 0.02)

            tamanho = estrela["tamanho"]

            self.coords(
                estrela["estrela_id"],
                estrela["x"] - tamanho,
                estrela["y"] - tamanho,
                estrela["x"] + tamanho,
                estrela["y"] + tamanho
            )

            self.coords(
                estrela["texto_id"],
                estrela["x"],
                estrela["y"] + 18
            )

        self.desenhar_linhas()
        self.after(30, self.animar)
