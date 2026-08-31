from peewee import *

db = SqliteDatabase("Alexandria.db")

class Usuário(Model):
    nome = CharField()
    password = CharField()

    class Meta:
        database = db
