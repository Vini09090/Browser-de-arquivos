from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import cm
from xml.sax.saxutils import escape


class Livros:
    """
    Funções relacionadas aos arquivos da biblioteca.

    Atualmente:
    - converte arquivos TXT para PDF.
    """

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
