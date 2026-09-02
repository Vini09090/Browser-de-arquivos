import customtkinter as ctk
from sistema_pesquisa import Pesquisa
from TelaExibição import Tela_exibição


class TelaPesquisa(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.geometry("800x650")
        self.title("Alexandria - Pesquisar Livros")

        self.pesquisa = Pesquisa()

        ctk.CTkLabel(
            self,
            text="Pesquisar Livros",
            font=("Arial", 24)
        ).pack(pady=20)


        self.area_pesquisa = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.area_pesquisa.pack(
            pady=30
        )


        self.entrada_pesquisa = ctk.CTkEntry(
            self.area_pesquisa,
            width=400,
            height=50,
            corner_radius=15,
            placeholder_text="Digite o nome do livro",
            font=("Arial", 15)
        )

        self.entrada_pesquisa.grid(
            row=0,
            column=0,
            padx=(0, 10)
        )

        self.botao_pesquisar = ctk.CTkButton(
            self.area_pesquisa,
            text="Pesquisar",
            width=130,
            height=50,
            corner_radius=15,
            command=self.realizar_pesquisa,
            fg_color="#004DD3",
            hover_color="#003AA3",
            font=("Arial", 15, "bold")
        )

        self.botao_pesquisar.grid(
            row=0,
            column=1
        )

        self.label_status = ctk.CTkLabel(
            self,
            text="",
            text_color="#aaaaaa"
        )
        self.label_status.pack(pady=10)

        self.entrada_pesquisa.bind("<Return>", lambda event: self.realizar_pesquisa())

    def realizar_pesquisa(self):
        termo = self.entrada_pesquisa.get().strip()

        if not termo:
            self.label_status.configure(
                text="Digite algo para pesquisar."
            )
            return

        resultados = self.pesquisa.realizar_pesquisa(termo)

        if not resultados:
            self.label_status.configure(
                text="Nenhum resultado encontrado."
            )
            return

        self.label_status.configure(
            text=f"{len(resultados)} resultados encontrados."
        )

        Tela_exibição(
            master=self,
            resultados=resultados
        )
