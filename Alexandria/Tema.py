import customtkinter as ctk
import json
from pathlib import Path

ARQUIVO_TEMA = Path(__file__).resolve().parent / "tema.json"


def obter_tema():
    try:
        if ARQUIVO_TEMA.exists():
            dados = json.loads(ARQUIVO_TEMA.read_text(encoding="utf-8"))
            tema = dados.get("tema", "Dark")
            if tema in ("Light", "Dark", "System"):
                return tema
    except Exception:
        pass

    return "Dark"


def definir_tema(tema):
    if tema not in ("Light", "Dark", "System"):
        tema = "Dark"

    ctk.set_appearance_mode(tema)

    try:
        ARQUIVO_TEMA.write_text(
            json.dumps({"tema": tema}, ensure_ascii=False, indent=4),
            encoding="utf-8"
        )
    except Exception:
        pass


def alternar_tema():
    novo_tema = "Light" if obter_tema() == "Dark" else "Dark"
    definir_tema(novo_tema)
    return novo_tema
