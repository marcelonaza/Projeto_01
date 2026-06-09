# 📈 Projeto 01 - E-Commerce Sales Analyzer

Este é um mini-projeto profissional de análise de dados estruturado em Python. O projeto utiliza o **Streamlit** para apresentar um dashboard web interativo, conecta-se a um banco de dados relacional e adota as melhores ferramentas de desenvolvimento do ecossistema Python moderno, como o gerenciador **uv** e o formatador/linter **Ruff**.

---

## 🚀 Funcionalidades

- **Dashboard Interativo (Streamlit):** Filtros dinâmicos por categorias de produtos e período de vendas, além de exibição de gráficos nativos e métricas chave (KPIs) de faturamento, quantidade vendida, ticket médio e total de vendas.
- **Relatório via Terminal (CLI):** Um ponto de entrada direto para visualizar métricas compiladas rapidamente de forma textual.
- **Suporte Multibanco de Dados:** Conexão nativa com PostgreSQL via Docker com fallback automático para SQLite local caso o PostgreSQL não esteja disponível.
- **Qualidade de Código Garantida:** Padronizado e validado utilizando o Ruff.

---

## 📁 Estrutura do Projeto

```text
Projeto_01/
├── data/
│   └── init.sql           # Script SQL para criar a tabela e popular dados de teste
├── src/
│   ├── __init__.py
│   ├── database.py        # Módulo de conexão com banco de dados (Postgres & SQLite)
│   └── analyzer.py        # Módulo de queries SQL e transformações Pandas
├── app.py                 # Painel interativo Streamlit (Web)
├── main.py                # Ponto de entrada CLI (Terminal)
├── docker-compose.yml     # Configuração do banco de dados PostgreSQL
├── pyproject.toml         # Configuração de pacotes (uv) e do Ruff
└── README.md              # Documentação do projeto
```

---

## 🛠️ Pré-requisitos

1. **Python 3.14+** gerenciado com o [uv](https://github.com/astral-sh/uv).
2. **Docker** (opcional, para rodar o banco PostgreSQL).

---

## ⚙️ Configuração Inicial

Antes de executar o projeto, configure as variáveis de ambiente:

1. **Copie o arquivo de exemplo:**
   ```bash
   cp .env.example .env
   ```

2. **Edite o arquivo `.env`** com suas credenciais do banco de dados:
   ```env
   PG_HOST=localhost
   PG_PORT=5432
   PG_DB=sales_db
   PG_USER=postgres
   PG_PASSWORD=sua_senha_aqui
   ```

> ⚠️ **Importante:** O arquivo `.env` contém credenciais sensíveis e **nunca deve ser versionado**. Ele já está incluído no `.gitignore`.

---

## 🏃 Como Executar o Projeto

O `uv` gerencia todas as dependências automaticamente para você, sem a necessidade de ativar manualmente um ambiente virtual.


### Opção A: Utilizando Banco de Dados SQLite (Sem Docker)
O projeto possui um mecanismo inteligente de fallback. Se você executar o projeto sem iniciar o contêiner do Docker, ele criará automaticamente um arquivo de banco de dados SQLite local chamado `sales.db` e o populará com os dados de teste contidos em `data/init.sql`.

1. **Para rodar o relatório resumido no terminal:**
   ```bash
   uv run main.py
   ```

2. **Para iniciar o dashboard Streamlit no navegador:**
   ```bash
   uv run streamlit run app.py
   ```

### Opção B: Utilizando PostgreSQL (Com Docker)
Caso você possua o Docker instalado, pode rodar o banco de dados oficial do projeto:

1. **Suba o contêiner do banco de dados:**
   ```bash
   docker compose up -d
   ```
   *Nota: O banco carregará o script SQL de população automática na primeira inicialização.*

2. **Rode a aplicação (Terminal ou Web):**
   ```bash
   uv run main.py
   # ou
   uv run streamlit run app.py
   ```

---

## 🔍 Qualidade de Código (Linter & Formatter)

Este projeto utiliza o **Ruff** para manter as boas práticas do Python (como PEP 8, imports limpos e legibilidade).

- **Verificar erros de qualidade (Linter):**
  ```bash
  uv run ruff check
  ```
- **Corrigir automaticamente erros corrigíveis:**
  ```bash
  uv run ruff check --fix
  ```
- **Formatar todo o código automaticamente:**
  ```bash
  uv run ruff format
  ```
