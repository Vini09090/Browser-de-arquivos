import customtkinter as ctk
import os
import webbrowser


class Tela_exibição(ctk.CTkToplevel):

    def __init__(self, master=None, resultados=None):
        super().__init__(master)

        self.geometry("900x700")
        self.title("Alexandria - Resultados")

        titulo = ctk.CTkLabel(
            self,
            text="Resultados da Pesquisa",
            font=("Arial", 24)
        )
        titulo.pack(pady=20)


        # Barra de progresso

        self.label_status = ctk.CTkLabel(
            self,
            text="Pesquisando...",
            text_color="#aaaaaa"
        )
        self.label_status.pack(pady=(0, 5))

        self.progress_bar = ctk.CTkProgressBar(
            self,
            width=500,
            mode="indeterminate"
        )
        self.progress_bar.pack(pady=(0, 10))

        self.progress_bar.start()


        self.frame_resultados = ctk.CTkScrollableFrame(
            self,
            width=800,
            height=440
        )

        self.frame_resultados.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )


        self.carregando = True

        # Os resultados podem ser enviados
        # diretamente ou posteriormente.
        if resultados is not None:
            self.exibir_resultados(resultados)


    def exibir_resultados(self, resultados):

        self.carregando = False

        # Para a barra
        self.progress_bar.stop()
        self.progress_bar.pack_forget()

        self.label_status.configure(
            text="Pesquisa concluída!"
        )

        resultados = resultados or []

        if not resultados:

            ctk.CTkLabel(
                self.frame_resultados,
                text="Nenhum livro encontrado.",
                font=("Arial", 16)
            ).pack(pady=20)

            return

        for livro in resultados:

            if not isinstance(livro, dict):
                continue

            titulo_livro = livro.get(
                "titulo",
                "Livro sem título"
            )

            url_livro = livro.get("url")

            if not url_livro:
                continue

            frame_livro = ctk.CTkFrame(
                self.frame_resultados
            )

            frame_livro.pack(
                fill="x",
                padx=10,
                pady=8
            )

            nome = ctk.CTkLabel(
                frame_livro,
                text=titulo_livro,
                font=("Arial", 14),
                anchor="w"
            )

            nome.pack(
                side="left",
                fill="x",
                expand=True,
                padx=15,
                pady=15
            )

            botao_abrir = ctk.CTkButton(
                frame_livro,
                text="Abrir",
                width=140,
                fg_color="#004DD3",
                hover_color="#0DD810",
                command=lambda url=url_livro:
                    self.abrir_livro(url)
            )

            botao_abrir.pack(
                side="right",
                padx=15,
                pady=10
            )


    def abrir_livro(self, url):

        if not url:
            return

        if os.path.exists(url):

            webbrowser.open(
                f"file://{os.path.abspath(url)}"
            )

        else:

            webbrowser.open(url)

