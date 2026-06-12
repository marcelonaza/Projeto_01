# 🎓 Guia de Estudos - E-Commerce Sales Analyzer

Bem-vindo ao guia de estudos do seu projeto! O objetivo deste documento é explicar detalhadamente cada tecnologia, conceito de arquitetura, arquivo e linha de código do **Projeto 01**. 

Ao final, você encontrará **desafios práticos** para implementar por conta própria e fixar o conhecimento.

---

## 🗺️ Índice
1. [Conceitos Gerais e Arquitetura](#1-conceitos-gerais-e-arquitetura)
2. [Gerenciador de Pacotes Moderno: `uv`](#2-gerenciador-de-pacotes-moderno-uv)
3. [Qualidade de Código e Formatação: `Ruff`](#3-qualidade-de-código-e-formatação-ruff)
4. [Banco de Dados: Postgres, SQLite e SQLAlchemy](#4-banco-de-dados-postgres-sqlite-e-sqlalchemy)
5. [Segurança e Configuração: `.env`](#5-segurança-e-configuração-env)
6. [Infraestrutura: Docker e Docker Compose](#6-infraestrutura-docker-e-docker-compose)
7. [Análise de Dados com Pandas](#7-análise-de-dados-com-pandas)
8. [Dashboard Interativo com Streamlit](#8-dashboard-interativo-com-streamlit)
9. [Controle de Versão com Git](#9-controle-de-versão-com-git)
10. [💪 Exercícios e Desafios Práticos](#-exercícios-e-desafios-práticos)

---

## 1. Conceitos Gerais e Arquitetura

O projeto adota uma arquitetura **modular**, que separa as responsabilidades da aplicação. Isso evita arquivos gigantes e difíceis de manter.

### A Estrutura de Pastas
```text
Projeto_01/
├── data/
│   └── init.sql           # Dados de teste para o banco PostgreSQL
├── src/
│   ├── __init__.py        # Transforma a pasta src em um pacote Python
│   ├── database.py        # Conexão com banco de dados (Postgres & SQLite)
│   └── analyzer.py        # Consultas SQL e lógica de negócios com Pandas
├── app.py                 # Interface Gráfica Web (Streamlit)
├── main.py                # Interface de Linha de Comando (CLI)
├── docker-compose.yml     # Configuração do banco Postgres no Docker
├── pyproject.toml         # Configurações do projeto, dependências e Ruff
├── .env / .env.example    # Gestão de credenciais e variáveis
└── .gitignore             # Arquivos ignorados pelo Git
```

- **Por que a pasta `src/`?** É um padrão de design em Python (src layout) que evita importações acidentais do código local durante testes e garante que o código seja empacotado corretamente.

---

## 2. Gerenciador de Pacotes Moderno: `uv`

Historicamente, o Python utilizou ferramentas como `pip`, `venv` e `requirements.txt`. Hoje em dia, ferramentas modernas como o `uv` (desenvolvido pela Astral) unificam tudo isso de forma extremamente rápida (escrita em Rust).

### O que o `uv` faz no projeto?
- **Gerencia a versão do Python:** Garante que todos rodem a mesma versão (definida em `.python-version`).
- **Gerencia ambientes virtuais:** Cria a pasta `.venv/` automaticamente sem você precisar digitar comandos complexos.
- **Instala pacotes com segurança:** Utiliza um arquivo de trava (`uv.lock`) para garantir que as versões instaladas sejam exatamente as mesmas em qualquer máquina.

### Comandos principais para você aprender:
- `uv init`: Inicializa um projeto Python moderno.
- `uv add <pacote>`: Instala uma biblioteca e a adiciona automaticamente ao `pyproject.toml` (ex: `uv add pandas`).
- `uv remove <pacote>`: Remove a biblioteca e limpa o arquivo de configurações.
- `uv run <script.py>`: Executa um script Python garantindo que o ambiente virtual esteja ativo e com todas as dependências instaladas. **Você não precisa mais ativar a venv manualmente!**

---

## 3. Qualidade de Código e Formatação: `Ruff`

O **Ruff** é um linter e formatador de código Python moderno e extremamente rápido (também escrito em Rust). Ele substitui ferramentas antigas como `flake8`, `black`, `isort` e `pylint`.

### Por que usar Linter e Formatador?
- **Linter (Análise Estática):** Varre seu código procurando por bugs em potencial, variáveis não utilizadas, imports esquecidos ou más práticas de programação.
- **Formatador:** Ajusta automaticamente espaçamentos, quebras de linha e padrão de aspas para que o código siga as diretrizes oficiais do Python (PEP 8).

### Configurações no `pyproject.toml`
Nós configuramos as seguintes regras no arquivo:
```toml
[tool.ruff.lint]
select = [
    "E",   # Erros de sintaxe/estilo (PEP8)
    "W",   # Avisos de estilo
    "F",   # Erros detectados pelo Pyflakes (ex: variáveis não usadas)
    "I",   # Organização de imports (isort)
    "B",   # Prevenção de bugs comuns (flake8-bugbear)
    "C90", # Complexidade ciclomática (evitar funções difíceis de ler)
]
```

### Comandos para praticar:
- `uv run ruff check`: Analisa o código e mostra erros.
- `uv run ruff check --fix`: Corrige erros simples automaticamente (ex: apaga imports não usados).
- `uv run ruff format`: Formata todo o código do projeto para o padrão estético profissional.

---

## 4. Banco de Dados: Postgres, SQLite e SQLAlchemy

O projeto utiliza a biblioteca **SQLAlchemy**, que é o ORM (Object Relational Mapper) mais popular do Python. 

### Por que usar SQLAlchemy e o conceito de Engine?
O SQLAlchemy cria uma abstração chamada `Engine` (motor). Com o mesmo código Python, você consegue conversar com diferentes bancos de dados (Postgres, MySQL, SQLite, Oracle) apenas alterando a string de conexão (URL).

### Como funciona o Fallback no arquivo `src/database.py`?
O código tenta se conectar ao PostgreSQL. Se der erro (ex: Docker desligado), ele captura a exceção e cria um banco SQLite local automaticamente:

```python
def get_db_engine() -> Engine:
    # 1. Tenta conectar no Postgres
    try:
        engine = create_engine(POSTGRES_URL, connect_args={"connect_timeout": 2})
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))  # Teste rápido de ping
        return engine
    except OperationalError:
        # 2. Fallback: Se falhar, usa SQLite local
        sqlite_engine = create_engine(SQLITE_URL)
        # Inicializa a tabela e insere dados falsos no SQLite
        setup_sqlite_database(sqlite_engine)
        return sqlite_engine
```

---

## 5. Segurança e Configuração: `.env`

Nunca coloque senhas ou chaves de acesso diretamente no código-fonte. Se você enviar isso para o GitHub, robôs podem rastrear suas credenciais em segundos.

### O Fluxo Profissional:
1. As credenciais reais ficam no arquivo `.env` (excluído do Git pelo `.gitignore`).
2. Um arquivo de modelo chamado `.env.example` é enviado ao Git, apenas ensinando quais variáveis o sistema precisa (sem as senhas reais).
3. No código, usamos a biblioteca `python-dotenv` para ler essas variáveis do sistema:
   ```python
   from dotenv import load_dotenv
   import os

   load_dotenv()  # Carrega as variáveis do arquivo .env
   db_password = os.getenv("PG_PASSWORD")
   ```

---

## 6. Infraestrutura: Docker e Docker Compose

O **Docker** cria "contêineres" isolados. Pense neles como computadores virtuais minimalistas que rodam apenas um serviço específico.

### O que o Docker Compose?
É uma ferramenta para definir e rodar aplicações multi-contêiner. Em vez de rodar linhas de comandos enormes para configurar o PostgreSQL, nós criamos o arquivo `docker-compose.yml`:

```yaml
services:
  db:
    image: postgres:16-alpine      # Imagem do Postgres leve
    environment:
      POSTGRES_DB: sales_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password123
    ports:
      - "5432:5432"                # Mapeia a porta do container para seu computador
    volumes:
      - ./data/init.sql:/docker-entrypoint-initdb.d/init.sql # Roda o script de dados inicial
```

Quando o Docker inicializa, qualquer script SQL dentro de `/docker-entrypoint-initdb.d/` é executado automaticamente. Por isso nosso `init.sql` popula o banco na primeira inicialização!

---

## 7. Análise de Dados com Pandas

O **Pandas** é a biblioteca padrão para manipulação e análise de dados em Python. No arquivo `src/analyzer.py`, usamos o Pandas integrado com o SQLAlchemy:

### Lendo dados do Banco de Dados:
```python
def load_sales_data(engine: Engine) -> pd.DataFrame:
    query = "SELECT * FROM sales;"
    # read_sql carrega o resultado da consulta diretamente em um DataFrame Pandas!
    return pd.read_sql(query, con=engine)
```

### Calculando Métricas com Pandas:
No Pandas, operamos sobre o DataFrame. Por exemplo:
- **Faturamento Total:** Soma da coluna de receita (`df["revenue"].sum()`).
- **Ticket Médio:** Receita média por item ou transação (`df["revenue"].mean()`).
- **Agrupamentos:** Para saber quais categorias vendem mais, agrupamos os dados:
  ```python
  df.groupby("category")["revenue"].sum().reset_index()
  ```

---

## 8. Dashboard Interativo com Streamlit

O **Streamlit** permite criar aplicações web interativas focadas em dados usando apenas Python (sem precisar escrever HTML, CSS ou Javascript).

### Ciclo de Execução do Streamlit:
**Importante:** Toda vez que o usuário interage com um botão, slider ou filtro na tela, o Streamlit **reexecuta o script inteiro de cima a baixo**.

### Principais componentes utilizados no `app.py`:
- `st.sidebar`: Cria um menu lateral.
- `st.selectbox` / `st.date_input`: Filtros interativos que retornam valores selecionados pelo usuário.
- `st.metric`: Exibe cartões de KPIs bonitos com setas de tendência.
- `st.line_chart` / `st.bar_chart`: Gera visualizações gráficas rápidas.

---

## 9. Controle de Versão com Git

O Git é a ferramenta que rastreia o histórico de alterações dos seus arquivos.

### O Fluxo Básico do Git:
1. **Working Directory (Seu código):** Onde você edita os arquivos.
2. **Staging Area (Preparação):** Você escolhe o que vai salvar no commit usando `git add .`.
3. **Local Repository (Histórico local):** Você grava as alterações permanentemente no seu computador com `git commit -m "mensagem"`.
4. **Remote Repository (GitHub):** Você envia o histórico local para a nuvem usando `git push`.

---

## 💪 Exercícios e Desafios Práticos

Para você aprender de verdade, você precisa colocar a mão na massa. Tente realizar estas tarefas no projeto:

### 🌟 Desafio 1: Adicionar um novo KPI no Dashboard (Fácil)
Adicione um cartão de métrica (KPI) no topo do painel do Streamlit (`app.py`) mostrando a **Quantidade Total de Itens Vendidos** (soma da coluna `quantity`).
- *Dica 1:* Adicione este campo no retorno do `get_summary_metrics` em `src/analyzer.py`.
- *Dica 2:* Exiba no `app.py` usando `st.metric`.

### 🌟 Desafio 2: Filtrar a tabela de dados brutos (Médio)
No final do arquivo `app.py`, existe uma seção de "Dados Brutos".
- Crie um checkbox `st.checkbox("Mostrar apenas vendas acima de R$ 500")`.
- Se o checkbox estiver marcado, filtre o DataFrame para exibir apenas linhas onde `revenue > 500`.

### 🌟 Desafio 3: Adicionar Gráfico de Vendas por Região (Difícil)
Nosso banco de dados contém uma coluna de `customer_region`.
- No arquivo `src/analyzer.py`, crie uma função que agrupe o faturamento por região.
- No arquivo `app.py`, adicione um gráfico de barras (`st.bar_chart`) mostrando o faturamento por região na tela principal.
