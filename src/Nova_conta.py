import customtkinter as ctk
from Dados.iniciar import perfil
from PIL import Image
from tkinter import messagebox

class Criar_conta(ctk.CTkToplevel):

    def __init__(self, master=None):
        super().__init__(master)


        self.geometry("1200x750")
        self.title("Nova Conta - Alexandria")
        imagem = Image.open("/home/vinicius/Alexandria1.0/Janelas/Imagens/Fundo_mar.jpeg")

        self.fundo = ctk.CTkImage(
            light_image=imagem,
            dark_image=imagem,
            size=(1200, 750)
        )

        self.label_fundo = ctk.CTkLabel(
            self,
            image=self.fundo,
            text=""
        )

        self.label_fundo.place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1
        )

        self.minsize(900, 600)
        self.resizable(True, True)

        # Tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Cor de fundo
        self.configure(fg_color="#0D0D0F")


        self.painel = ctk.CTkFrame(
            self,
            width=430,
            height=560,
            corner_radius=25,
            fg_color="#161619",
            border_width=1,
            border_color="#2A2A2F"
        )

        self.painel.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        self.painel.pack_propagate(False)


        self.titulo = ctk.CTkLabel(
            self.painel,
            text="Nova conta",
            font=("Arial", 30, "bold"),
            text_color="#FFFFFF"
        )

        self.titulo.pack(
            pady=(45, 5)
        )


        self.subtitulo = ctk.CTkLabel(
            self.painel,
            text="Crie sua conta para acessar o Alexandria",
            font=("Arial", 14),
            text_color="#92929A"
        )

        self.subtitulo.pack(
            pady=(0, 35)
        )

        self.label_usuario = ctk.CTkLabel(
            self.painel,
            text="Nome de usuário",
            font=("Arial", 13, "bold"),
            text_color="#DADAE0",
            anchor="w"
        )

        self.label_usuario.pack(
            fill="x",
            padx=55,
            pady=(0, 7)
        )

        self.entrada_usuario = ctk.CTkEntry(
            self.painel,
            width=320,
            height=48,
            corner_radius=12,
            placeholder_text="Digite seu nome de usuário",
            placeholder_text_color="#707078",
            font=("Arial", 14),
            fg_color="#202024",
            border_color="#34343A",
            border_width=1
        )

        self.entrada_usuario.pack(
            padx=55,
            pady=(0, 20)
        )


        self.label_senha = ctk.CTkLabel(
            self.painel,
            text="Senha",
            font=("Arial", 13, "bold"),
            text_color="#DADAE0",
            anchor="w"
        )

        self.label_senha.pack(
            fill="x",
            padx=55,
            pady=(0, 7)
        )

        self.senha = ctk.CTkEntry(
            self.painel,
            width=320,
            height=48,
            corner_radius=12,
            placeholder_text="Digite sua senha",
            placeholder_text_color="#707078",
            font=("Arial", 14),
            fg_color="#202024",
            border_color="#34343A",
            border_width=1,
            show="*"
        )

        self.senha.pack(
            padx=55,
            pady=(0, 12)
        )

        self.mostrar_senha = ctk.BooleanVar(value=False)

        self.checkbox = ctk.CTkCheckBox(
            self.painel,
            text="Mostrar senha",
            variable=self.mostrar_senha,
            command=self.alternar_senha,
            font=("Arial", 12),
            text_color="#A0A0A8",
            fg_color="#2E6BE6",
            hover_color="#1F5AC7",
            border_color="#55555E"
        )

        self.checkbox.pack(
            anchor="w",
            padx=55,
            pady=(0, 25)
        )



        self.button = ctk.CTkButton(
            self.painel,
            text="Criar conta",
            command=self.adicionar_perfil,
            width=320,
            height=50,
            corner_radius=12,
            border_width=0,
            fg_color="#2E6BE6",
            hover_color="#1F5AC7",
            font=("Arial", 16, "bold")
        )

        self.button.pack(
            padx=55,
            pady=(0, 20)
        )

        self.info = ctk.CTkLabel(
            self.painel,
            text="Seus dados serão armazenados com segurança.",
            font=("Arial", 11),
            text_color="#66666F"
        )

        self.info.pack(
            pady=(0, 10)
        )

    def alternar_senha(self):

        if self.mostrar_senha.get():
            self.senha.configure(show="")
        else:
            self.senha.configure(show="*")



    def adicionar_perfil(self):

        pessoa = self.entrada_usuario.get()
        password = self.senha.get()
        pessoa = perfil(nome = pessoa , senha= password)
        pessoa.criar_conta()
        return messagebox.showinfo("Alexandria" ,"Sua conta foi criada com sucesso!!!")
        



if __name__ == "__main__":
    app = Criar_conta()
    app.mainloop()