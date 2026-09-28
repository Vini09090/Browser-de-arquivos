import requests
from bs4 import BeautifulSoup
from urllib.parse import quote


class BuscadorDeLivros:

    def __init__(self):
        self.TIMEOUT = 10
        self.fontes = [
            self.GoogleBooks,
            self.Gutenberg,
            self.Internet_Archive,
            self.OpenLibrary,
            self.WikiSource,
            self.OAPEN,
            self.LibriVox,
            self.DOAB
        ]

    def GoogleBooks(self, titulo: str, limite: int = 10) -> dict:
        URL = "https://www.googleapis.com/books/v1/volumes"
        parametros = {
            "q": f'intitle:{titulo}',
            "maxResults": limite,
            "printType": "books",
        }

        try:
            resposta = requests.get(URL, params=parametros, timeout=self.TIMEOUT)
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
                timeout=self.TIMEOUT
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
                timeout=self.TIMEOUT
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

    def OpenLibrary(self, titulo: str, limite: int = 10) -> dict:
        parametros = {"title": titulo, "limit": limite}

        try:
            resposta = requests.get(
                "https://openlibrary.org/search.json",
                params=parametros,
                headers={"User-Agent": "SistemaBiblioteca/1.0 (projeto educacional)"},
                timeout=self.TIMEOUT
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
                timeout=self.TIMEOUT
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
                "url": "https://pt.wikisource.org/wiki/" + quote(nome.replace(" ", "_")),
                "download": None,
            })

        return {"fonte": "Wikisource", "resultados": resultados}

    def OAPEN(self, titulo: str, limite: int = 10) -> dict:
        url = "https://library.oapen.org/rest/search"
        params = {
            "query": titulo,
            "expand": "metadata,bitstreams",
            "limit": limite,
        }
        headers = {"Accept": "application/json"}

        try:
            resp = requests.get(url, params=params, headers=headers, timeout=self.TIMEOUT)
            resp.raise_for_status()
            dados = resp.json()
        except (requests.RequestException, ValueError) as e:
            return {"fonte": "OAPEN Library", "resultados": [], "erro": str(e)}

        resultados = []
        if isinstance(dados, list):
            for item in dados:
                nome = item.get("name")
                handle = item.get("handle")
                if not nome or not handle:
                    continue

                resultados.append({
                    "fonte": "OAPEN Library",
                    "encontrado": True,
                    "titulo": nome,
                    "autor": [],
                    "ano": None,
                    "isbn": [],
                    "idioma": [],
                    "descricao": handle,
                    "url": f"https://library.oapen.org/handle/{handle}",
                    "download": None,
                })

        return {"fonte": "OAPEN Library", "resultados": resultados}

    def LibriVox(self, titulo: str, limite: int = 10) -> dict:
        url = "https://librivox.org/api/feed/audiobooks"
        params = {"format": "json", "limit": limite, "title": titulo}

        try:
            resp = requests.get(url, params=params, timeout=self.TIMEOUT)
            resp.raise_for_status()
            dados = resp.json()
        except (requests.RequestException, ValueError) as e:
            return {"fonte": "LibriVox", "resultados": [], "erro": str(e)}

        resultados = []
        livros = dados.get("books", []) if isinstance(dados, dict) else []

        for livro in livros:
            nome = livro.get("title")
            url_livro = livro.get("url_librivox")
            if not nome or not url_livro:
                continue

            autor = f"{livro.get('author_first_name', '')} {livro.get('author_last_name', '')}".strip()

            resultados.append({
                "fonte": "LibriVox",
                "encontrado": True,
                "titulo": nome,
                "autor": [autor] if autor else [],
                "ano": livro.get("copyright_year"),
                "isbn": [],
                "idioma": [livro.get("language")] if livro.get("language") else [],
                "descricao": livro.get("description"),
                "url": url_livro,
                "download": livro.get("url_zip_file"),
            })

        return {"fonte": "LibriVox", "resultados": resultados}

    def DOAB(self, titulo: str, limite: int = 10) -> dict:
        url = "https://directory.doabooks.org/rest/search"
        params = {
            "query": titulo,
            "expand": "metadata,bitstreams",
            "limit": limite,
        }
        headers = {"Accept": "application/json"}

        try:
            resp = requests.get(url, params=params, headers=headers, timeout=self.TIMEOUT)
            resp.raise_for_status()
            dados = resp.json()
        except (requests.RequestException, ValueError) as e:
            return {"fonte": "DOAB", "resultados": [], "erro": str(e)}

        resultados = []
        if isinstance(dados, list):
            for item in dados:
                nome = item.get("name")
                handle = item.get("handle")
                if not nome or not handle:
                    continue

                resultados.append({
                    "fonte": "DOAB",
                    "encontrado": True,
                    "titulo": nome,
                    "autor": [],
                    "ano": None,
                    "isbn": [],
                    "idioma": [],
                    "descricao": handle,
                    "url": f"https://directory.doabooks.org/handle/{handle}",
                    "download": None,
                })

        return {"fonte": "DOAB", "resultados": resultados}

    def buscar_em_todas(self, titulo: str = "", limite: int = 5, title: str = None, limit: int = None) -> list:
        termo_busca = title if title is not None else titulo
        limite_busca = limit if limit is not None else limite

        resultados = []

        for fonte in self.fontes:
            try:
                resultado = fonte(titulo=termo_busca, limite=limite_busca)

                if isinstance(resultado, dict):
                    resultados.append(resultado)

            except Exception as erro:
                resultados.append({
                    "fonte": getattr(fonte, "__name__", "Desconhecida"),
                    "resultados": [],
                    "erro": str(erro)
                })

        return resultados
