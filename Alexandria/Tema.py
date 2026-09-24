import customtkinter as ctk

modo_atual = "Dark"


def alternar_tema():
    global modo_atual

    if modo_atual == "Dark":
        modo_atual = "Light"
    else:
        modo_atual = "Dark"

    ctk.set_appearance_mode(modo_atual)


def definir_tema(modo):
    global modo_atual

    modo_atual = modo
    ctk.set_appearance_mode(modo)


def obter_tema():
    return modo_atual
