from pathlib import Path

from PIL import Image, ImageEnhance


class GerenciadorImagem:

    def __init__(self, caminho):
        self.caminho = Path(caminho)

        if not self.caminho.exists():
            raise FileNotFoundError(
                f"Imagem não encontrada:\n{self.caminho}"
            )

        # Guarda SEMPRE a imagem original
        self.original = Image.open(
            self.caminho
        ).convert("RGB")

    def cover(self, largura, altura):
        """
        Faz a imagem preencher completamente
        a área sem deformá-la.
        """

        if largura <= 0 or altura <= 0:
            return self.original.copy()

        imagem = self.original.copy()

        img_largura, img_altura = imagem.size

        escala = max(
            largura / img_largura,
            altura / img_altura
        )

        nova_largura = int(img_largura * escala)
        nova_altura = int(img_altura * escala)

        imagem = imagem.resize(
            (nova_largura, nova_altura),
            Image.Resampling.LANCZOS
        )

        esquerda = (nova_largura - largura) // 2
        topo = (nova_altura - altura) // 2

        imagem = imagem.crop(
            (
                esquerda,
                topo,
                esquerda + largura,
                topo + altura
            )
        )

        return imagem

    def preparar(
        self,
        largura,
        altura,
        brilho=1.0,
        saturacao=1.0
    ):
        """
        Cria uma nova imagem a partir da original.
        """

        imagem = self.cover(
            largura,
            altura
        )

        if brilho != 1.0:
            imagem = ImageEnhance.Brightness(
                imagem
            ).enhance(brilho)

        if saturacao != 1.0:
            imagem = ImageEnhance.Color(
                imagem
            ).enhance(saturacao)

        return imagem
