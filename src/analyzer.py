from typing import TypedDict

import pandas as pd
from sqlalchemy import Engine


class SalesMetrics(TypedDict):
    """Estrutura tipada para as métricas de vendas."""

    total_revenue: float
    total_quantity: int
    avg_ticket: float
    total_orders: int


def load_sales_data(engine: Engine) -> pd.DataFrame:
    """Carrega as vendas brutas do banco de dados e calcula o faturamento.

    Args:
        engine: Instância do engine do SQLAlchemy.

    Returns:
        pd.DataFrame: DataFrame contendo as vendas tratadas.
    """
    query = (
        "SELECT id, sale_date, product_name, quantity, unit_price, category FROM sales"
    )
    df = pd.read_sql_query(query, con=engine)

    # Conversão de tipos de dados para segurança
    df["sale_date"] = pd.to_datetime(df["sale_date"])
    df["quantity"] = df["quantity"].astype(int)
    df["unit_price"] = df["unit_price"].astype(float)

    # Calcula o faturamento total (Receita) de cada linha
    df["total_revenue"] = df["quantity"] * df["unit_price"]

    return df


def get_summary_metrics(df: pd.DataFrame) -> SalesMetrics:
    """Calcula métricas principais de vendas (KPIs).

    Args:
        df: DataFrame tratado obtido de load_sales_data.

    Returns:
        dict: Dicionário com receita, itens, ticket médio e transações.
    """
    if df.empty:
        return {
            "total_revenue": 0.0,
            "total_quantity": 0,
            "avg_ticket": 0.0,
            "total_orders": 0,
        }

    total_revenue = df["total_revenue"].sum()
    total_quantity = df["quantity"].sum()
    total_orders = len(df)
    avg_ticket = total_revenue / total_orders if total_orders > 0 else 0.0

    return {
        "total_revenue": total_revenue,
        "total_quantity": total_quantity,
        "avg_ticket": avg_ticket,
        "total_orders": total_orders,
    }


def get_sales_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega receita e quantidade por categoria.

    Args:
        df: DataFrame de vendas.

    Returns:
        pd.DataFrame: DataFrame agregado por categoria.
    """
    if df.empty:
        return pd.DataFrame(columns=["category", "total_revenue", "quantity"])

    return (
        df.groupby("category")[["total_revenue", "quantity"]]
        .sum()
        .reset_index()
        .sort_values(by="total_revenue", ascending=False)
    )


def get_sales_by_product(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega receita e quantidade por produto.

    Args:
        df: DataFrame de vendas.

    Returns:
        pd.DataFrame: DataFrame agregado por produto.
    """
    if df.empty:
        return pd.DataFrame(columns=["product_name", "total_revenue", "quantity"])

    return (
        df.groupby("product_name")[["total_revenue", "quantity"]]
        .sum()
        .reset_index()
        .sort_values(by="total_revenue", ascending=False)
    )


def get_sales_trends(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega receita por mês para visualização de tendências.

    Args:
        df: DataFrame de vendas.

    Returns:
        pd.DataFrame: DataFrame com evolução de receita mensal.
    """
    if df.empty:
        return pd.DataFrame(columns=["month", "total_revenue"])

    # Cria coluna formatada como 'Ano-Mês'
    df_trends = df.copy()
    df_trends["month"] = df_trends["sale_date"].dt.to_period("M").astype(str)

    return (
        df_trends.groupby("month")[["total_revenue"]]
        .sum()
        .reset_index()
        .sort_values(by="month")
    )
