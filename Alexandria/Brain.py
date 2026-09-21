from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import cm
from xml.sax.saxutils import escape
from pathlib import Path
import shutil

#criar função que transfere um arquivo de um lugar para o outro.
# Cria uma pasta chamada biblioteca, se ela já existe evita a criação.

class Livros:
    """
    Funções relacionadas aos arquivos da biblioteca.

    Atualmente:
    - converte arquivos TXT para PDF.
    """

    def localizar_arquivos(self, caminho: str, nome: str):
        """
        Procura um arquivo pelo nome dentro da pasta
        e de todas as suas subpastas.
        """

        pasta = Path(caminho)

        if not pasta.exists() or not pasta.is_dir():
            return None

        # Procura pelo nome em todas as subpastas
        for arquivo in pasta.rglob(nome):

            if arquivo.is_file():
                return arquivo

        return None

    def mover_arquivos(self,destino: str,caminho_atual: str, nome: str):
        """
        Procura um arquivo pelo nome, independente da pasta,
        e move para a biblioteca.
        """

        destino = Path(destino)

        # Procura o arquivo pelo nome
        arquivo = self.localizar_arquivos(
            caminho_atual,
            nome
        )

        if arquivo is None:
            print(f"Arquivo não encontrado: {nome}")
            return False

        # Cria a biblioteca se ela não existir
        destino.mkdir(
            parents=True,
            exist_ok=True
        )

        # Caminho final
        destino_arquivo = destino / arquivo.name

        # Evita sobrescrever outro arquivo
        if destino_arquivo.exists():
            print(
                f"O arquivo já existe na biblioteca: "
                f"{destino_arquivo}"
            )
            return False

        try:

            shutil.move(
                str(arquivo),
                str(destino_arquivo)
            )

            print(
                f"Arquivo movido para: "
                f"{destino_arquivo}"
            )

            return True

        except OSError as erro:

            print(f"Erro ao mover o arquivo: {erro}")

            return False
    
    @staticmethod
    def converter_txt_para_pdf(arquivo_txt: str, arquivo_pdf: str) -> bool:
        """
        Converte um arquivo .txt em um arquivo .pdf.

        Retorna:
            True  -> conversão realizada com sucesso.
            False -> ocorreu algum erro.
        """

        try:
            with open(arquivo_txt, "r", encoding="utf-8") as arquivo:
                conteudo = arquivo.read()

            documento = SimpleDocTemplate(
                arquivo_pdf,
                pagesize=A4,
                rightMargin=2 * cm,
                leftMargin=2 * cm,
                topMargin=2 * cm,
                bottomMargin=2 * cm
            )

            estilos = getSampleStyleSheet()

            estilo_texto = estilos["BodyText"]
            estilo_texto.alignment = TA_LEFT
            estilo_texto.leading = 16
            estilo_texto.fontName = "Helvetica"
            estilo_texto.fontSize = 11

            elementos = []

            # Mantém as quebras de linha do arquivo TXT.
            paragrafos = conteudo.split("\n")

            for linha in paragrafos:
                linha = escape(linha)

                if linha.strip():
                    elementos.append(
                        Paragraph(linha, estilo_texto)
                    )
                else:
                    elementos.append(
                        Spacer(1, 0.3 * cm)
                    )

            # Evita gerar um PDF completamente vazio.
            if not elementos:
                elementos.append(
                    Paragraph("", estilo_texto)
                )

            documento.build(elementos)

            return True

        except (OSError, UnicodeDecodeError):
            return False
        except Exception as erro:
            print(f"Erro ao converter TXT para PDF: {erro}")
            return False

    def usuarios(self, senha :str , usuário : str ) -> str:
        with open("usuários.txt", "w") as arquivo:
            arquivo.write(f"{usuário} : {senha}")
            arquivo.close()
