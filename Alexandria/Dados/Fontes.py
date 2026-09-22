import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

# Termos online, requisitados.
class BuscadorDeLivros:

    def __init__(self):
        self.fontes = [
            self.GoogleBooks,
            self.Gutenberg,
            self.Internet_Archive,
            self.OpenLibary,
            self.WikiSource,
        ]

    def GoogleBooks(self, titulo: str, limite: int = 10) -> dict:
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
        except (requests.RequestException, ValueError) as erro:
            return {"fonte": "Google Books", "resultados": [], "erro": str(erro)}

        resultados = []

        for item in dados.get("items", []):
            info = item.get("volumeInfo", {})
            acesso = item.get("accessInfo", {})

            url = info.get("infoLink")
            if not info.get("title") or not url:
                continue

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
                "url": url,
                "download": acesso.get("pdf", {}).get("downloadLink"),
                "dominio_publico": acesso.get("publicDomain", False),
            })

        return {"fonte": "Google Books", "resultados": resultados}

    def Gutenberg(self, titulo: str, limite: int = 10) -> dict:
        url = f"https://www.gutenberg.org/ebooks/search/?query={quote(titulo)}"

        try:
            resposta = requests.get(
                url,
                headers={"User-Agent": "SistemaBiblioteca/1.0"},
                timeout=15
            )
            resposta.raise_for_status()
        except requests.RequestException as erro:
            return {"fonte": "Project Gutenberg", "resultados": [], "erro": str(erro)}

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

            if not nome or not href:
                continue

            resultados.append({
                "fonte": "Project Gutenberg",
                "encontrado": True,
                "titulo": nome,
                "autor": [autor] if autor else [],
                "ano": None,
                "isbn": [],
                "idioma": [],
                "descricao": None,
                "url": f"https://www.gutenberg.org{href}",
                "download": None,
            })

        return {"fonte": "Project Gutenberg", "resultados": resultados}

    def Internet_Archive(self, titulo: str, limite: int = 10) -> dict:
        parametros = [
            ("q", f'title:("{titulo}") AND mediatype:texts'),
            ("fl[]", "identifier"), ("fl[]", "title"),
            ("fl[]", "creator"), ("fl[]", "date"),
            ("fl[]", "description"), ("fl[]", "language"),
            ("rows", limite), ("page", 1), ("output", "json")
        ]

        try:
            resposta = requests.get(
                "https://archive.org/advancedsearch.php",
                params=parametros,
                timeout=15
            )
            resposta.raise_for_status()
            dados = resposta.json()
        except (requests.RequestException, ValueError) as erro:
            return {"fonte": "Internet Archive", "resultados": [], "erro": str(erro)}

        resultados = []

        for livro in dados.get("response", {}).get("docs", []):
            identifier = livro.get("identifier")
            if not identifier:
                continue

            autores = livro.get("creator", [])
            idiomas = livro.get("language", [])

            if isinstance(autores, str):
                autores = [autores]
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
                "url": f"https://archive.org/details/{identifier}",
                "download": None,
            })

        return {"fonte": "Internet Archive", "resultados": resultados}

    def OpenLibary(self, titulo: str, limite: int = 10) -> dict:
        parametros = {"title": titulo, "limit": limite}

        try:
            resposta = requests.get(
                "https://openlibrary.org/search.json",
                params=parametros,
                headers={"User-Agent": "SistemaBiblioteca/1.0 (projeto educacional)"},
                timeout=10
            )
            resposta.raise_for_status()
            dados = resposta.json()
        except (requests.RequestException, ValueError) as erro:
            return {"fonte": "Open Library", "resultados": [], "erro": str(erro)}

        resultados = []

        for livro in dados.get("docs", []):
            chave = livro.get("key")
            if not chave or not livro.get("title"):
                continue

            resultados.append({
                "fonte": "Open Library",
                "encontrado": True,
                "titulo": livro.get("title"),
                "autor": livro.get("author_name", []),
                "ano": livro.get("first_publish_year"),
                "isbn": livro.get("isbn", [])[:10],
                "idioma": livro.get("language", []),
                "descricao": None,
                "url": f"https://openlibrary.org{chave}",
                "download": None,
            })

        return {"fonte": "Open Library", "resultados": resultados}

    def WikiSource(self, titulo: str, limite: int = 10) -> dict:
        parametros = {
            "action": "query",
            "list": "search",
            "srsearch": titulo,
            "format": "json",
            "srlimit": limite,
        }

        try:
            resposta = requests.get(
                "https://pt.wikisource.org/w/api.php",
                params=parametros,
                timeout=10
            )
            resposta.raise_for_status()
            dados = resposta.json()
        except (requests.RequestException, ValueError) as erro:
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
                "url": "https://pt.wikisource.org/wiki/" + nome.replace(" ", "_"),
                "download": None,
            })

        return {"fonte": "Wikisource", "resultados": resultados}

    def buscar_em_todas(self, title: str, limit: int = 5, headless: bool = True) -> list:
        resultados = []

        for fonte in self.fontes:
            try:
                resultado = fonte(titulo=title, limite=limit)

                if isinstance(resultado, dict):
                    resultados.append(resultado)

            except Exception as erro:
                resultados.append({
                    "fonte": fonte.__name__,
                    "resultados": [],
                    "erro": str(erro)
                })

        return resultados


if __name__ == "__main__":
    buscador = BuscadorDeLivros()
    resultados = buscador.buscar_em_todas("Dom Casmurro", limit=5)

    for item in resultados:
        print(
            f"Fonte: {item['fonte']} | "
            f"Encontrados: {len(item.get('resultados', []))}"
        )
