# Browser de Livros

O **Browser de Livros** é uma aplicação desenvolvida para facilitar a organização, localização e pesquisa de livros armazenados no computador.

O programa permite pesquisar livros dentro de uma determinada pasta ou em um conjunto de várias pastas, apresentando os resultados por meio de uma interface gráfica mais organizada e intuitiva.

O principal objetivo do projeto é facilitar o gerenciamento de grandes quantidades de arquivos. Como diferencial, caso um livro não seja encontrado nos arquivos locais, o sistema também permite realizar pesquisas em **domínios públicos e bibliotecas digitais**, ampliando as possibilidades de encontrar o conteúdo procurado.

## Funcionalidades

* Pesquisa de livros em uma pasta específica.
* Pesquisa em múltiplas pastas.
* Exibição organizada dos resultados encontrados.
* Pesquisa em fontes e domínios públicos quando o livro não está disponível localmente.
* Sistema de login.
* Perfil de usuário salvo na primeira utilização.
* Sistema de anotações.
* Rede neural.
* Configurações da aplicação.
* Interface gráfica para facilitar a utilização do programa.

## Funcionamento da pesquisa

O fluxo básico da pesquisa de livros funciona da seguinte maneira:

```text
Tela_pesquisa.py
       │
       ▼
Pesquisa.realizar_pesquisa()
       │
       ▼
   Resultados
       │
       ▼
Tela_exibição
```

A pesquisa é iniciada pela interface `Tela_pesquisa.py`, que chama o método `Pesquisa.realizar_pesquisa()`.

Após a realização da pesquisa, os resultados encontrados são encaminhados para a tela de exibição, onde podem ser apresentados ao usuário.

## Sistema de Login

Nesta versão do projeto, o sistema de login também é responsável por salvar o perfil do usuário durante o primeiro acesso.

O fluxo principal da aplicação pode ser representado da seguinte forma:

```text
Login
  │
  ▼
TelaLogin
  │
  ▼
App
  ├── Pesquisa de livros
  ├── Anotações
  ├── Rede Neural
  └── Configurações
```

Após a autenticação, o usuário é direcionado para a aplicação principal, onde pode acessar as diferentes funcionalidades disponíveis.

## Estrutura do projeto

A estrutura principal de funcionamento do Browser de Livros é organizada da seguinte maneira:

```text
main.py
   │
   ▼
Sistema_Login.py
   │
   ▼
TelaLogin
   │
   ▼
app.py
   │
   ├───────────────┬────────────────┐
   ▼               ▼                ▼
Pesquisa        Anotações        Rede Neural
   │
   ▼
sistema_pesquisa.py
```

### Principais arquivos

| Arquivo               | Função                                            |
| --------------------- | ------------------------------------------------- |
| `main.py`             | Ponto de entrada da aplicação.                    |
| `Sistema_Login.py`    | Responsável pelo sistema de login.                |
| `app.py`              | Inicializa e organiza a aplicação principal.      |
| `Tela_pesquisa.py`    | Interface responsável pela pesquisa de livros.    |
| `sistema_pesquisa.py` | Contém a lógica principal do sistema de pesquisa. |

## Download

Para baixar o projeto, utilize o Git para clonar o repositório:

```bash
git clone URL_DO_REPOSITORIO
```

Depois, entre na pasta do projeto:

```bash
cd nome-do-projeto
```

> Substitua `URL_DO_REPOSITORIO` pelo endereço do repositório no GitHub e `nome-do-projeto` pelo nome da pasta criada.

### Download pelo GitHub

Também é possível baixar o projeto diretamente pelo GitHub:

1. Acesse a página do repositório.
2. Clique no botão **Code**.
3. Selecione **Download ZIP**.
4. Extraia o arquivo `.zip`.
5. Abra a pasta do projeto em seu editor de código ou terminal.

## Instalação

Caso o projeto utilize Python, recomenda-se criar um ambiente virtual antes de instalar as dependências:

```bash
python -m venv venv
```

No Windows:

```bash
venv\Scripts\activate
```

No Linux:

```bash
source venv/bin/activate
```

Depois, instale as dependências do projeto:

```bash
pip install -r requirements.txt
```

Caso o projeto não possua um arquivo `requirements.txt`, instale manualmente as bibliotecas utilizadas pelo projeto.

## Execução

Após a instalação das dependências, execute o arquivo principal:

```bash
python main.py
```

O sistema deverá iniciar a tela de login e, após a autenticação, disponibilizar as funcionalidades da aplicação.

## Status do projeto

O **Browser de Livros** encontra-se em desenvolvimento. Algumas funcionalidades ainda podem sofrer alterações ou receber melhorias em versões futuras.

## Objetivo do projeto

O projeto busca unir **organização de arquivos, pesquisa de livros e acesso a fontes públicas** em uma única aplicação, proporcionando uma maneira mais prática e visual de localizar e gerenciar materiais de estudo.

---

**Browser de Livros** — organização, pesquisa e acesso a livros em uma única aplicação.
