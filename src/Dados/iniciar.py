from .banco import db, Usuário

db.connect()
db.create_tables([Usuário])

class perfil:
    def __init__(self, nome, senha):
        self.nome = nome
        self.senha = senha

    def criar_conta(self) -> bool:
        try:
            Usuário.create(
                nome=self.nome,
                password=self.senha
            )
            return True
        except:
            return False

    def verificar(self) -> bool:
        usuario = Usuário.get_or_none(
            (Usuário.nome == self.nome) &
            (Usuário.password == self.senha)
        )

        return usuario is not None
