from playwright.sync_api import sync_playwright
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

#Criar resultados e por filtar as informações adqueadas 

class BuscadorDeLivros:
    def __init__(self):
        pass
        
    def BiblioSP(self, titulo: str, limite: int = 10, headless: bool = True) -> dict:
        """
        Pesquisa no BiblioSP usando um navegador real.

        Esta versão é propositalmente exploratória: ela abre o catálogo,
        preenche a pesquisa e retorna o texto da página. Isso permite testar
        a interação real antes de criar seletores específicos para cada campo.
        """
        resultados = []
        URL = (
        "https://bibliotecacircula.prefeitura.sp.gov.br/"
        "pesquisa/pesquisaAvancada.xhtml")

        try:
            with sync_playwright() as p:
                navegador = p.chromium.launch(headless=headless)
                pagina = navegador.new_page()

                try:
                    pagina.goto(URL, wait_until="networkidle", timeout=30000)

                    campo = pagina.get_by_placeholder(
                        "Busque por obras, autores e assuntos"
                    )
                    campo.fill(titulo)

                    pagina.get_by_text("Pesquisar", exact=True).click()
                    pagina.wait_for_load_state("networkidle")

                    corpo = pagina.locator("body").inner_text()

                    resultados.append({
                        "fonte": "BiblioSP",
                        "encontrado": "Encontrados: 0" not in corpo,
                        "titulo": titulo,
                        "autor": [],
                        "ano": None,
                        "isbn": [],
                        "idioma": [],
                        "descricao": None,
                        "url": pagina.url,
                        "download": None,
                        "texto_pagina": corpo[:5000],
                    })
                finally:
                    navegador.close()

        except Exception as erro:
            return {
                "fonte": "BiblioSP",
                "resultados": [],
                "erro": str(erro),
            }

        return {"fonte": "BiblioSP", "resultados": resultados}

    def Dominio_pulbico(self,titulo: str, limite: int = 10, headless: bool = True) -> dict:
        """
        Abre a pesquisa do Domínio Público do MEC.

        O portal utiliza uma aplicação legada. Por isso esta primeira versão
        apenas abre o formulário e coleta o HTML/texto para permitir identificar
        os campos reais antes de automatizar o envio.
        """
        resultados = []
        URL = (
            "https://dominiopublico.mec.gov.br/"
            "pesquisa/PesquisaObraForm.do"
        )
        try:
            with sync_playwright() as p:
                navegador = p.chromium.launch(headless=headless)
                pagina = navegador.new_page()

                try:
                    pagina.goto(URL, wait_until="networkidle", timeout=30000)

                    corpo = pagina.locator("body").inner_text()

                    resultados.append({
                        "fonte": "Domínio Público MEC",
                        "encontrado": False,
                        "titulo": titulo,
                        "autor": [],
                        "ano": None,
                        "isbn": [],
                        "idioma": [],
                        "descricao": None,
                        "url": pagina.url,
                        "download": None,
                        "texto_pagina": corpo[:5000],
                        "status": "formulario_aberto",
                    })
                finally:
                    navegador.close()

        except Exception as erro:
            return {
                "fonte": "Domínio Público MEC",
                "resultados": [],
                "erro": str(erro),
            }

        return {"fonte": "Domínio Público MEC", "resultados": resultados}


    def GoogleBooks(self,titulo: str, limite: int = 10) -> dict:
        """Pesquisa livros no Google Books."""

        URL = "https://www.googleapis.com/books/v1/volumes"

        parametros = {
            "q": f'intitle:{titulo}',
            "maxResults": limite,
            "printType": "books",
        }

        try:
            resposta = requests.get(URL, params=parametros, timeout=10)
            resposta.raise_for_status()
            dados = resposta.json()
        except requests.RequestException as erro:
            return {"fonte": "Google Books", "resultados": [], "erro": str(erro)}

        resultados = []

        for item in dados.get("items", []):
            info = item.get("volumeInfo", {})
            acesso = item.get("accessInfo", {})

            isbn = [
                x.get("identifier")
                for x in info.get("industryIdentifiers", [])
                if x.get("identifier")
            ]

            resultados.append({
                "fonte": "Google Books",
                "encontrado": True,
                "titulo": info.get("title"),
                "autor": info.get("authors", []),
                "ano": info.get("publishedDate"),
                "isbn": isbn,
                "idioma": [info["language"]] if info.get("language") else [],
                "descricao": info.get("description"),
                "url": info.get("infoLink"),
                "download": acesso.get("pdf", {}).get("downloadLink"),
                "dominio_publico": acesso.get("publicDomain", False),
            })

        return {"fonte": "Google Books", "resultados": resultados}


    def Gutenberg(self,titulo: str, limite: int = 10) -> dict:
        """Pesquisa obras no catálogo do Project Gutenberg."""
        url = (
            "https://www.gutenberg.org/ebooks/search/"
            f"?query={quote(titulo)}"
        )

        headers = {"User-Agent": "SistemaBiblioteca/1.0"}

        try:
            resposta = requests.get(url, headers=headers, timeout=15)
            resposta.raise_for_status()
        except requests.RequestException as erro:
            return {
                "fonte": "Project Gutenberg",
                "resultados": [],
                "erro": str(erro),
            }

        soup = BeautifulSoup(resposta.text, "html.parser")
        resultados = []

        for item in soup.select("li.booklink")[:limite]:
            link = item.select_one("a.link")
            titulo_html = item.select_one("span.title")
            autor_html = item.select_one("span.subtitle")

            if not link:
                continue

            nome = titulo_html.get_text(strip=True) if titulo_html else None
            autor = autor_html.get_text(strip=True) if autor_html else None
            href = link.get("href")

            resultados.append({
                "fonte": "Project Gutenberg",
                "encontrado": True,
                "titulo": nome,
                "autor": [autor] if autor else [],
                "ano": None,
                "isbn": [],
                "idioma": [],
                "descricao": None,
                "url": f"https://www.gutenberg.org{href}" if href else None,
                "download": None,
            })

        return {"fonte": "Project Gutenberg", "resultados": resultados}


    def Internet_Archive(self,titulo: str, limite: int = 10) -> dict:
        """Pesquisa textos/livros no Internet Archive."""
        parametros = [
            ("q", f'title:("{titulo}") AND mediatype:texts'),
            ("fl[]", "identifier"),
            ("fl[]", "title"),
            ("fl[]", "creator"),
            ("fl[]", "date"),
            ("fl[]", "description"),
            ("fl[]", "language"),
            ("rows", limite),
            ("page", 1),
            ("output", "json"),
        ]
        URL = "https://archive.org/advancedsearch.php"
        try:
            resposta = requests.get(URL, params=parametros, timeout=15)
            resposta.raise_for_status()
            dados = resposta.json()
        except requests.RequestException as erro:
            return {"fonte": "Internet Archive", "resultados": [], "erro": str(erro)}

        resultados = []

        for livro in dados.get("response", {}).get("docs", []):
            identifier = livro.get("identifier")
            url = f"https://archive.org/details/{identifier}" if identifier else None

            autores = livro.get("creator", [])
            if isinstance(autores, str):
                autores = [autores]

            idiomas = livro.get("language", [])
            if isinstance(idiomas, str):
                idiomas = [idiomas]

            resultados.append({
                "fonte": "Internet Archive",
                "encontrado": True,
                "titulo": livro.get("title"),
                "autor": autores,
                "ano": livro.get("date"),
                "isbn": [],
                "idioma": idiomas,
                "descricao": livro.get("description"),
                "url": url,
                "download": None,
            })

        return {"fonte": "Internet Archive", "resultados": resultados}


    def OpenLibary(self,titulo: str, limite: int = 10) -> dict:
        """Pesquisa livros na Open Library."""
        parametros = {
            "title": titulo,
            "limit": limite,
        }
        URL = "https://openlibrary.org/search.json"
        headers = {
            "User-Agent": "SistemaBiblioteca/1.0 (projeto educacional)"
        }

        try:
            resposta = requests.get(
                URL, params=parametros, headers=headers, timeout=10
            )
            resposta.raise_for_status()
            dados = resposta.json()
        except requests.RequestException as erro:
            return {"fonte": "Open Library", "resultados": [], "erro": str(erro)}

        resultados = []

        for livro in dados.get("docs", []):
            chave = livro.get("key")
            url = f"https://openlibrary.org{chave}" if chave else None

            resultados.append({
                "fonte": "Open Library",
                "encontrado": True,
                "titulo": livro.get("title"),
                "autor": livro.get("author_name", []),
                "ano": livro.get("first_publish_year"),
                "isbn": livro.get("isbn", [])[:10],
                "idioma": livro.get("language", []),
                "descricao": None,
                "url": url,
                "download": None,
            })

        return {"fonte": "Open Library", "resultados": resultados}


    def WikiSource(self,titulo: str, limite: int = 10) -> dict:

        """Pesquisa páginas relacionadas a uma obra no Wikisource."""
        parametros = {
            "action": "query",
            "list": "search",
            "srsearch": titulo,
            "format": "json",
            "srlimit": limite,
        }
        URL = "https://pt.wikisource.org/w/api.php"
        try:
            resposta = requests.get(URL, params=parametros, timeout=10)
            resposta.raise_for_status()
            dados = resposta.json()
        except requests.RequestException as erro:
            return {"fonte": "Wikisource", "resultados": [], "erro": str(erro)}

        resultados = []

        for item in dados.get("query", {}).get("search", []):
            nome = item.get("title")
            if not nome:
                continue

            resultados.append({
                "fonte": "Wikisource",
                "encontrado": True,
                "titulo": nome,
                "autor": [],
                "ano": None,
                "isbn": [],
                "idioma": ["pt"],
                "descricao": None,
                "url": (
                    "https://pt.wikisource.org/wiki/"
                    + nome.replace(" ", "_")
                ),
                "download": None,
            })

        return {"fonte": "Wikisource", "resultados": resultados}

    
    def main(self, title: str, limit: int = 10, headless: bool = True) -> list:
            
            """Executa todas as buscas em sequência chamando os métodos com self."""
            resultados = [
            self.BiblioSP(titulo= title, limite= 10, headless=headless),
            self.Dominio_pulbico(titulo= title, limite= limit, headless= headless),
            self.GoogleBooks(titulo= title, limite= limit),
            self.Gutenberg(titulo= title , limite= limit),
            self.Internet_Archive(titulo=title , limite=limit),
            self.OpenLibary(titulo= title , limite= limit), 
            self.WikiSource(titulo= title , limite= limit)]
        
            return resultados


if __name__ == "__main__":
    buscador = BuscadorDeLivros()
    resultados = buscador.buscar_em_todas(title ="Dom Casmurro", limit=5)

    for item in resultados:
        print(f"Fonte: {item['fonte']} | Encontrados: {len(item.get('resultados', []))}")


# Na hora da execução vai aparecer os resultados, logo no sistema de pesquisa online deveria aparecer apenas as opções online.
#Fonte: BiblioSP | Encontrados: 1
#Fonte: Domínio Público MEC | Encontrados: 0
#Fonte: Google Books | Encontrados: 0
#Fonte: Project Gutenberg | Encontrados: 1
#Fonte: Internet Archive | Encontrados: 5
#Fonte: Open Library | Encontrados: 5
#Fonte: Wikisource | Encontrados: 0
