import customtkinter as ctk
from sistema_pesquisa import Pesquisa
from .TelaExibição import Tela_exibição
import threading

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
            width=460,
            height=50,
            corner_radius=15,
            placeholder_text="Digite o nome do livro",
            font=("Arial", 19)
        )

        self.entrada_pesquisa.grid(
            row=0,
            column=0,
            padx=(0, 10)
        )

        self.botao_pesquisar = ctk.CTkButton(
            self.area_pesquisa,
            text="Pesquisar",
            width=145,
            height=50,
            corner_radius=18,
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

        # Evita iniciar várias pesquisas ao mesmo tempo
        self.botao_pesquisar.configure(
            state="disabled",
            text="Pesquisando..."
        )

        self.label_status.configure(
            text="Iniciando pesquisa..."
        )

        # Cria a janela de resultados imediatamente
        self.janela_resultados = Tela_exibição(
            master=self
        )

        # Executa a pesquisa em uma thread separada
        threading.Thread(
            target=self.executar_pesquisa,
            args=(termo,),
            daemon=True
        ).start()


    def executar_pesquisa(self, termo):
        """
        Essa função roda fora da thread principal.
        """

        resultados = self.pesquisa.realizar_pesquisa(termo)

        # Depois que a pesquisa terminar,
        # volta para a thread da interface.
        self.after(
            0,
            lambda: self.finalizar_pesquisa(resultados)
        )


    def finalizar_pesquisa(self, resultados):

        self.botao_pesquisar.configure(
            state="normal",
            text="Pesquisar"
        )

        if not resultados:
            self.label_status.configure(
                text="Nenhum resultado encontrado."
            )

            self.janela_resultados.exibir_resultados([])

            return

        self.label_status.configure(
            text=f"{len(resultados)} resultados encontrados."
        )

        # Atualiza a janela de resultados
        self.janela_resultados.exibir_resultados(
            resultados
        )

