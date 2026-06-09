import streamlit as st

from src.analyzer import (
    get_sales_by_category,
    get_sales_by_product,
    get_sales_trends,
    get_summary_metrics,
    load_sales_data,
)
from src.database import get_db_engine

# 1. Configuração da página Streamlit
st.set_page_config(
    page_title="Dashboard de Vendas - Projeto 01",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Dashboard de Vendas - E-Commerce")
st.markdown("Dashboard interativo conectado a banco de dados relacional.")
st.markdown("---")


# 2. Obtenção dos dados utilizando cache para performance
@st.cache_resource
def get_cached_engine():
    return get_db_engine()


engine = get_cached_engine()

try:
    df_raw = load_sales_data(engine)
except Exception as e:
    st.error(f"Erro ao carregar dados do banco: {e}")
    st.stop()

# 3. Barra lateral (Sidebar) com filtros interativos
st.sidebar.header("Filtros de Análise")

# Filtro de Período de Vendas (Datas)
min_date = df_raw["sale_date"].min().date()
max_date = df_raw["sale_date"].max().date()
date_range = st.sidebar.date_input(
    "Período de Vendas",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

# Filtro de Categoria de Produtos
categories = sorted(df_raw["category"].unique())
selected_categories = st.sidebar.multiselect(
    "Categorias de Produtos",
    options=categories,
    default=categories,
)

# Processa o intervalo de datas selecionado
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = end_date = date_range

# Aplica os filtros ao DataFrame bruto
df_filtered = df_raw[
    (df_raw["sale_date"].dt.date >= start_date)
    & (df_raw["sale_date"].dt.date <= end_date)
    & (df_raw["category"].isin(selected_categories))
]

# 4. Verifica se existem registros após aplicar os filtros
if df_filtered.empty:
    st.warning("⚠️ Nenhum registro encontrado para os filtros selecionados.")
else:
    # Calcula as métricas resumidas
    metrics = get_summary_metrics(df_filtered)

    # 5. Painel de KPIs (Métricas Principais)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label="Faturamento Total",
            value=f"R$ {metrics['total_revenue']:,.2f}".replace(",", "X")
            .replace(".", ",")
            .replace("X", "."),
        )
    with col2:
        st.metric(
            label="Itens Vendidos",
            value=f"{metrics['total_quantity']:,}".replace(",", "."),
        )
    with col3:
        st.metric(
            label="Ticket Médio por Venda",
            value=f"R$ {metrics['avg_ticket']:,.2f}".replace(",", "X")
            .replace(".", ",")
            .replace("X", "."),
        )
    with col4:
        st.metric(
            label="Total de Pedidos",
            value=f"{metrics['total_orders']:,}".replace(",", "."),
        )

    st.markdown("---")

    # 6. Abas organizacionais para análise detalhada
    tab1, tab2, tab3 = st.tabs(
        [
            "📊 Evolução & Tendências",
            "🏷️ Categoria & Produtos",
            "📋 Tabela de Dados Brutos",
        ]
    )

    with tab1:
        st.subheader("Evolução Mensal do Faturamento")
        df_trends = get_sales_trends(df_filtered)

        # Gráfico de linhas nativo do Streamlit para tendência mensal
        st.line_chart(
            data=df_trends.set_index("month"),
            y="total_revenue",
            use_container_width=True,
        )

    with tab2:
        col_cat, col_prod = st.columns(2)

        with col_cat:
            st.subheader("Receita Total por Categoria")
            df_cat = get_sales_by_category(df_filtered)
            st.bar_chart(
                data=df_cat.set_index("category"),
                y="total_revenue",
                use_container_width=True,
            )

        with col_prod:
            st.subheader("Ranking de Produtos por Receita")
            df_prod = get_sales_by_product(df_filtered)

            # Formata DataFrame para exibição elegante
            df_prod_styled = df_prod.copy()
            df_prod_styled["total_revenue"] = df_prod_styled["total_revenue"].apply(
                lambda val: f"R$ {val:,.2f}"
            )
            st.dataframe(
                df_prod_styled.rename(
                    columns={
                        "product_name": "Produto",
                        "total_revenue": "Receita Gerada",
                        "quantity": "Qtd. Vendida",
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )

    with tab3:
        st.subheader("Listagem das Vendas")
        # Formatando datas e valores antes de exibir na tabela
        df_display = df_filtered[
            [
                "sale_date",
                "product_name",
                "category",
                "quantity",
                "unit_price",
                "total_revenue",
            ]
        ].copy()
        df_display["sale_date"] = df_display["sale_date"].dt.strftime("%d/%m/%Y")
        df_display["unit_price"] = df_display["unit_price"].apply(
            lambda val: f"R$ {val:,.2f}"
        )
        df_display["total_revenue"] = df_display["total_revenue"].apply(
            lambda val: f"R$ {val:,.2f}"
        )

        st.dataframe(
            df_display.rename(
                columns={
                    "sale_date": "Data da Venda",
                    "product_name": "Nome do Produto",
                    "category": "Categoria",
                    "quantity": "Qtd.",
                    "unit_price": "Preço Unitário",
                    "total_revenue": "Total da Venda",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )
