import customtkinter as ctk
import os
import webbrowser


class Tela_exibição(ctk.CTkToplevel):

    def __init__(self, master=None, resultados=None):
        super().__init__(master)

        self.geometry("850x600")
        self.minsize(700, 450)
        self.title("Brain - Resultados")

        titulo = ctk.CTkLabel(
            self,
            text="Resultados da Pesquisa",
            font=("Arial", 24)
        )
        titulo.pack(pady=(20, 10))

        self.frame_resultados = ctk.CTkScrollableFrame(
            self,
            width=760,
            height=480
        )
        self.frame_resultados.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(10, 20)
        )

        # Garante que a tela aceite somente resultados no formato:
        # {"titulo": "...", "url": "..."}
        resultados_validos = []

        if resultados:
            for livro in resultados:

                if not isinstance(livro, dict):
                    continue

                titulo_livro = livro.get("titulo")
                url_livro = livro.get("url")

                if not titulo_livro or not url_livro:
                    continue

                resultados_validos.append({
                    "titulo": titulo_livro,
                    "url": url_livro
                })

        if not resultados_validos:
            vazio = ctk.CTkLabel(
                self.frame_resultados,
                text="Nenhum livro encontrado.",
                font=("Arial", 15)
            )
            vazio.pack(pady=20)
            return

        for livro in resultados_validos:

            frame_livro = ctk.CTkFrame(
                self.frame_resultados
            )

            frame_livro.pack(
                fill="x",
                padx=10,
                pady=8
            )

            frame_livro.grid_columnconfigure(0, weight=1)

            nome = ctk.CTkLabel(
                frame_livro,
                text=livro["titulo"],
                font=("Arial", 14),
                anchor="w"
            )

            nome.grid(
                row=0,
                column=0,
                sticky="ew",
                padx=15,
                pady=15
            )

            botao_abrir = ctk.CTkButton(
                frame_livro,
                text="Abrir",
                width=90,
                command=lambda url=livro["url"]: self.abrir_livro(url),
                fg_color="green",
                hover_color="darkgreen"
            )

            botao_abrir.grid(
                row=0,
                column=1,
                padx=15,
                pady=10
            )

    def abrir_livro(self, url):

        if not url:
            return

        # ARQUIVO LOCAL
        if os.path.exists(url):
            webbrowser.open(
                f"file://{os.path.abspath(url)}"
            )

        # LINK ONLINE
        else:
            webbrowser.open(url)
