from peewee import *
import os
#from Configurações import Configuracoes

def iniciar_banco():
    db.connect(reuse_if_open=True)
    db.create_tables([Usuário])


def verificar_pasta(nome :str):
    if os.path.exists(nome):
        return True
    else:
        return False

db = SqliteDatabase("Dados/Alexandria.db")

class Usuário(Model):
    nome = CharField(unique=True)
    password = CharField(unique=True)   
   

    class Meta:
        database = db

class Arquivos(Model):
    extensao = CharField(null=True)
    caminho = CharField()
    categoria = CharField()

    class Meta:
        database = db


