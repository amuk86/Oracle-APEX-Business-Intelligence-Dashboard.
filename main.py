import os
import threading
import webbrowser

from configer import OUTPUT_FILENAME
from chartProducts  import build_products_chart
from chartCustomers import build_customers_chart
from chartOrders    import build_orders_chart
from chartInventory import build_inventory_chart
from chartSales     import build_sales_chart
from llm_query       import run_query_loop


# --- HTML EXPORT ---

def save_dashboard(figures: dict, output_path: str) -> None:
    html_divs = []
    include_js = "cdn"
    for fig in figures.values():
        html_divs.append(fig.to_html(full_html=False, include_plotlyjs=include_js))
        include_js = False

    cards = "".join(f'<div class="chart-card">{div}</div>' for div in html_divs)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Oracle APEX Business Dashboard</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f0f2f5;
            margin: 0;
            padding: 20px;
        }}
        h1 {{ text-align: center; color: #333; margin-bottom: 30px; }}
        .dashboard-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));
            gap: 20px;
            max-width: 1400px;
            margin: 0 auto;
        }}
        .chart-card {{
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 15px;
            overflow: hidden;
        }}
    </style>
</head>
<body>
    <h1>Business Overview Dashboard</h1>
    <div class="dashboard-grid">{cards}</div>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    abs_path = os.path.abspath(output_path)
    print(f"\n Dashboard successfully created: {abs_path}")
    print(" Opening in browser...")
    webbrowser.open(f"file://{abs_path}")


# --- ENTRY POINT ---

def main():
    print("Fetching data and generating charts...")

    builders = {
        "products":  build_products_chart,
        "customers": build_customers_chart,
        "orders":    build_orders_chart,
        "inventory": build_inventory_chart,
        "sales":     build_sales_chart,
    }

    figures = {
        key: fig
        for key, builder in builders.items()
        if (fig := builder()) is not None
    }

    if not figures:
        print("No charts could be generated. Check your API connections.")
        return

    print("\nGenerating final HTML file...")
    save_dashboard(figures, OUTPUT_FILENAME)

    # --- LAUNCH LLM QUERY INTERFACE IN BACKGROUND THREAD ---
    # daemon=True ensures the thread exits automatically when main exits
    llm_thread = threading.Thread(target=run_query_loop, daemon=True)
    llm_thread.start()
    llm_thread.join()   # Keep main alive until the user types 'exit'


if __name__ == "__main__":
    main()
