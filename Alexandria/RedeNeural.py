import customtkinter as ctk
import math
import os
import random
import webbrowser
from arquivos_integrado import Janela_arquivos


class TelaRedeNeural(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.geometry("1200x800")
        self.title("Alexandria - Rede Neural")
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
            text="＋  Adicionar arquivo",
            width=165,
            height=38,
            corner_radius=8,
            fg_color="#202020",
            hover_color="#303030",
            text_color="white",
            font=("Arial", 13, "bold"),
            command=self.adicionar_arquivo
        ).pack(side="right", padx=(10, 20))

        # Botão voltar
        ctk.CTkButton(
            self.header,
            text="← Voltar",
            width=100,
            height=38,
            corner_radius=8,
            fg_color="transparent",
            hover_color="#242424",
            text_color="#E8F716",
            font=ctk.CTkFont(size=14),
            command=self.destroy
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
            text="Cada ponto representa um livro da sua biblioteca",
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

        self.constelacao = ConstelacaoCanvas(
            self.rede_frame,
            pasta_livros="/home/vinicius/Documentos/Biblioteca",
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

        ctk.CTkLabel(
            self.info_frame,
            text="● Rede ativa",
            font=("Arial", 13, "bold"),
            text_color="#E8F716"
        ).pack(side="left", padx=(5, 15))

        self.atualizar_contador()

    def atualizar_contador(self):
        quantidade = len(self.constelacao.estrelas)

        self.contador_label.configure(
            text=f"📚  {quantidade} arquivos conectados"
        )

    def adicionar_arquivo(self):
        if __name__ == "__main__":
            app = Janela_arquivos(self)
            app.mainloop()
        
   

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
        # Novos arquivos entram pela região inferior da rede,
        # dando a sensação de que estão sendo acrescentados à animação.
        x = random.randint(80, self.width - 80)
        y = random.randint(max(80, self.height - 150), self.height - 80)

        tamanho = random.randint(3, 5)
        vx = random.uniform(-0.3, 0.3)
        vy = random.uniform(-0.3, 0.3)

        estrela_id = self.create_oval(
            x - tamanho,
            y - tamanho,
            x + tamanho,
            y + tamanho,
            fill="yellow",
            outline=""
        )

        texto_id = self.create_text(
            x,
            y + 18,
            text=nome[:25],
            fill="#898686",
            font=("Arial", 10)
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
ap = TelaRedeNeural()
ap.mainloop()
