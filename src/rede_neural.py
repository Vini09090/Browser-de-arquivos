import customtkinter as ctk
import math
import os
import random
import webbrowser


class TelaRedeNeural(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.geometry("1200x800")
        self.title("Alexandria - Rede Neural")
        self.configure(fg_color="#090909")

        ctk.CTkLabel(
            self,
            text="REDE DE CONHECIMENTO",
            font=("Arial", 30, "bold"),
            text_color="white"
        ).pack(pady=(20, 10))

        ctk.CTkLabel(
            self,
            text="Cada ponto representa um livro da sua biblioteca",
            font=("Arial", 16),
            text_color="#a1a1aa"
        ).pack(pady=(0, 20))

        self.constelacao = ConstelacaoCanvas(
            self,
            pasta_livros="/home/vinicius/Biblioteca",
            width=1100,
            height=620
        )
        self.constelacao.pack(pady=20)

        quantidade = len(self.constelacao.estrelas)

        ctk.CTkLabel(
            self,
            text=f"{quantidade} arquivos conectados",
            font=("Arial", 14),
            text_color="#71717a"
        ).pack(pady=5)

        ctk.CTkButton(
            self,
            text="⬅ Voltar",
            width=120,
            command=self.destroy
        ).pack(pady=10)


class ConstelacaoCanvas(ctk.CTkCanvas):
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
        self.linhas = []

        self.carregar_livros()
        self.animar()

    def carregar_livros(self):
        if not os.path.isdir(self.pasta_livros):
            return

        for raiz, _, arquivos in os.walk(self.pasta_livros):
            for arquivo in arquivos:
                if arquivo.lower().endswith((".pdf", ".txt", ".epub")):
                    self.criar_estrela(
                        arquivo,
                        os.path.join(raiz, arquivo)
                    )

    def criar_estrela(self, nome, caminho):
        x = random.randint(80, self.width - 80)
        y = random.randint(80, self.height - 80)

        tamanho = random.randint(3, 5)
        vx = random.uniform(-0.3, 0.3)
        vy = random.uniform(-0.3, 0.3)

        estrela_id = self.create_oval(
            x - tamanho,
            y - tamanho,
            x + tamanho,
            y + tamanho,
            fill="white",
            outline=""
        )

        texto_id = self.create_text(
            x,
            y + 18,
            text=nome[:25],
            fill="#bdbdbd",
            font=("Arial", 9)
        )

        estrela = {
            "x": x,
            "y": y,
            "vx": vx,
            "vy": vy,
            "tamanho": tamanho,
            "nome": nome,
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

        self.estrelas.append(estrela)

    def abrir_arquivo(self, caminho):
        if os.path.exists(caminho):
            webbrowser.open(f"file://{os.path.abspath(caminho)}")

    def desenhar_linhas(self):
        for linha in self.linhas:
            self.delete(linha)

        self.linhas.clear()

        for i, estrela1 in enumerate(self.estrelas):
            for estrela2 in self.estrelas[i + 1:]:
                distancia = math.hypot(
                    estrela1["x"] - estrela2["x"],
                    estrela1["y"] - estrela2["y"]
                )

                if distancia < 140:
                    linha = self.create_line(
                        estrela1["x"],
                        estrela1["y"],
                        estrela2["x"],
                        estrela2["y"],
                        fill="#3B82F6",
                        width=1
                    )
                    self.linhas.append(linha)

    def animar(self):
        for estrela in self.estrelas:
            estrela["x"] += estrela["vx"]
            estrela["y"] += estrela["vy"]

            if estrela["x"] <= 40 or estrela["x"] >= self.width - 40:
                estrela["vx"] *= -1

            if estrela["y"] <= 40 or estrela["y"] >= self.height - 40:
                estrela["vy"] *= -1

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
