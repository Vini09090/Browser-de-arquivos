from peewee import *
import os

def verificar_pasta(nome :str):
    if os.path.exists(nome):
        return True
    else:
        return False

db = SqliteDatabase("Alexandria.db")

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


