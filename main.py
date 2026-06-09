import sys

from src.analyzer import get_summary_metrics, load_sales_data
from src.database import get_db_engine


def main():
    print("=== Iniciando Análise de Vendas ===")
    try:
        engine = get_db_engine()
        df = load_sales_data(engine)
        metrics = get_summary_metrics(df)

        print("\n--- RESUMO DE VENDAS ---")
        print(f"Faturamento Total: R$ {metrics['total_revenue']:,.2f}")
        print(f"Itens Vendidos: {metrics['total_quantity']}")
        print(f"Ticket Médio: R$ {metrics['avg_ticket']:,.2f}")
        print(f"Total de Vendas: {metrics['total_orders']}")
        print("------------------------\n")
        print("Para ver o dashboard completo no navegador, execute:")
        print("  uv run streamlit run app.py")

    except Exception as e:
        print(f"Erro ao executar a análise: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
