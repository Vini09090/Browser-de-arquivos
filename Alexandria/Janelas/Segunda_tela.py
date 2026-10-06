
import os
import customtkinter as ctk
from Dados.Brain import Livros
from pathlib import Path
from Dados.Configurações import Configuracoes


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

PASTA_BIBLIOTECA = Path.home() / "Biblioteca"
configurações = Configuracoes()


class TelaSecundaria(ctk.CTkToplevel):

    def __init__(self, master=None):
        super().__init__(master)

        self.geometry("950x850")
        self.minsize(850, 750)
        self.title("Alexandria - Anotações")
        self.configure(fg_color="#0B0B0B")

        self.categorias = configurações.obter_categorias()

        if not self.categorias:
            self.categorias = ["Geral"]

        self.criar_interface()

    def criar_interface(self):

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.cabecalho = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.cabecalho.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=40,
            pady=(30, 15)
        )

        self.cabecalho.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.cabecalho,
            text="Nova anotação",
            font=("Arial", 30, "bold"),
            text_color="#FFFFFF"
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkLabel(
            self.cabecalho,
            text="Crie uma anotação e organize-a em sua biblioteca.",
            font=("Arial", 14),
            text_color="#888888"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=(5, 0)
        )

        self.container_principal = ctk.CTkFrame(
            self,
            corner_radius=18,
            fg_color="#151515"
        )
        self.container_principal.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=40,
            pady=(0, 15)
        )

        self.container_principal.grid_columnconfigure(0, weight=1)
        self.container_principal.grid_rowconfigure(2, weight=1)

  

        self.frame_informacoes = ctk.CTkFrame(
        self.container_principal,
        fg_color="transparent"
    )
        self.frame_informacoes.grid(
                row=0,
                column=0,
                sticky="ew",
                padx=30,
                pady=(30, 10)
            )

        self.frame_informacoes.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.frame_informacoes,
            text="Título",
            font=("Arial", 13, "bold"),
            text_color="#BBBBBB"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 6)
        )

        ctk.CTkLabel(
            self.frame_informacoes,
            text="Categoria",
            font=("Arial", 13, "bold"),
            text_color="#BBBBBB"
        ).grid(
            row=0,
            column=1,
            sticky="w",
            padx=(15, 0),
            pady=(0, 6)
        )

        self.entry_titulo = ctk.CTkEntry(
            self.frame_informacoes,
            placeholder_text="Digite o título da anotação...",
            height=45,
            corner_radius=10,
            border_width=1,
            border_color="#333333",
            fg_color="#0D0D0D"
        )
        self.entry_titulo.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        self.menu_categorias = ctk.CTkOptionMenu(
            self.frame_informacoes,
            values=self.categorias,
            width=150,
            height=45,
            corner_radius=10,
            fg_color="#1F7A3A",
            button_color="#17632E",
            button_hover_color="#238A44",
            dropdown_fg_color="#181818",
            dropdown_hover_color="#2A2A2A"
        )
        self.menu_categorias.grid(
            row=1,
            column=1,
            padx=(15, 0)
        )

        self.frame_editor = ctk.CTkFrame(
            self.container_principal,
            fg_color="transparent"
        )
        self.frame_editor.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=30,
            pady=(10, 20)
        )

        self.frame_editor.grid_columnconfigure(0, weight=1)
        self.frame_editor.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            self.frame_editor,
            text="Conteúdo",
            font=("Arial", 13, "bold"),
            text_color="#BBBBBB"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 6)
        )

        self.entrada_nota = ctk.CTkTextbox(
            self.frame_editor,
            corner_radius=12,
            border_width=1,
            border_color="#333333",
            fg_color="#0D0D0D",
            font=("Arial", 15),
            wrap="word"
        )
        self.entrada_nota.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        self.frame_acoes = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.frame_acoes.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=40,
            pady=(0, 10)
        )

        self.frame_acoes.grid_columnconfigure(0, weight=1)

        self.label_status = ctk.CTkLabel(
            self.frame_acoes,
            text="Pronto para criar sua anotação.",
            font=("Arial", 13),
            text_color="#777777"
        )
        self.label_status.grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.frame_botoes = ctk.CTkFrame(
            self.frame_acoes,
            fg_color="transparent"
        )
        self.frame_botoes.grid(
            row=0,
            column=1,
            sticky="e"
        )

        ctk.CTkButton(
            self.frame_botoes,
            text="Limpar",
            command=self.limpar_nota,
            width=120,
            height=45,
            corner_radius=10,
            fg_color="#555353",
            hover_color="#C43D3D",
            text_color="#FFFFFF"
        ).pack(
            side="left",
            padx=(0, 10)
        )

        ctk.CTkButton(
            self.frame_botoes,
            text="Salvar TXT",
            command=self.salvar_nota,
            width=140,
            height=45,
            corner_radius=10,
            fg_color="#20A83A",
            hover_color="#18852D",
            text_color="#FFFFFF"
        ).pack(
            side="left",
            padx=(0, 10)
        )

        ctk.CTkButton(
            self.frame_botoes,
            text="Exportar PDF",
            command=self.exportar_pdf,
            width=150,
            height=45,
            corner_radius=10,
            fg_color="#1769AA",
            hover_color="#12568C",
            text_color="#FFFFFF"
        ).pack(
            side="left"
        )

    def obter_titulo(self):
        titulo = self.entry_titulo.get().strip()

        if not titulo:
            return "Minha_Nota"

        caracteres_invalidos = '<>:"/\\|?*'

        for caractere in caracteres_invalidos:
            titulo = titulo.replace(caractere, "_")

        return titulo

    def obter_caminho_categoria(self):
        categoria = self.menu_categorias.get()

        pasta_categoria = PASTA_BIBLIOTECA / categoria
        pasta_categoria.mkdir(
            parents=True,
            exist_ok=True
        )

        return pasta_categoria

    def salvar_nota(self):

        texto = self.entrada_nota.get(
            "1.0",
            "end"
        ).strip()

        if not texto:
            self.label_status.configure(
                text="Digite algum conteúdo antes de salvar.",
                text_color="#E05A5A"
            )
            return

        pasta_categoria = self.obter_caminho_categoria()
        titulo = self.obter_titulo()

        arquivo_txt = pasta_categoria / f"{titulo}.txt"

        with open(
            arquivo_txt,
            "w",
            encoding="utf-8"
        ) as arquivo:
            arquivo.write(texto)

        self.label_status.configure(
            text=f"Nota salva em {arquivo_txt.name}",
            text_color="#20A83A"
        )

    def exportar_pdf(self):

        texto = self.entrada_nota.get(
            "1.0",
            "end"
        ).strip()

        if not texto:
            self.label_status.configure(
                text="Digite algum conteúdo antes de exportar.",
                text_color="#E05A5A"
            )
            return

        pasta_categoria = self.obter_caminho_categoria()
        titulo = self.obter_titulo()

        arquivo_txt = pasta_categoria / f"{titulo}.txt"
        arquivo_pdf = pasta_categoria / f"{titulo}.pdf"

        with open(
            arquivo_txt,
            "w",
            encoding="utf-8"
        ) as arquivo:
            arquivo.write(texto)

        sucesso = Livros.converter_txt_para_pdf(
            str(arquivo_txt),
            str(arquivo_pdf)
        )

        if sucesso:
            self.label_status.configure(
                text=f"PDF criado em {arquivo_pdf.name}",
                text_color="#20A83A"
            )
        else:
            self.label_status.configure(
                text="Erro ao gerar PDF.",
                text_color="#E05A5A"
            )

    def limpar_nota(self):

        self.entry_titulo.delete(
            0,
            "end"
        )

        self.entrada_nota.delete(
            "1.0",
            "end"
        )

        self.label_status.configure(
            text="Editor limpo.",
            text_color="#777777"
        )


if __name__ == "__main__":
    app = TelaSecundaria()
    app.mainloop()
