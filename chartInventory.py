import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from configer import URLS
from fetcher import fetch_data


def build_inventory_chart() -> go.Figure | None:
    """Inventory Distribution Across Warehouses — bar chart."""
    df = fetch_data(URLS["inventory"])
    if df.empty:
        return None

    num_col = df.select_dtypes(include=["number"]).columns
    if len(num_col) == 0:
        num_col = df.columns[-1]
        df[num_col] = pd.to_numeric(df[num_col], errors="coerce")
    else:
        num_col = num_col[0]

    label_col = df.select_dtypes(exclude=["number"]).columns[0]

    fig = px.bar(
        df, x=label_col, y=num_col,
        title="Inventory Distribution Across Warehouses",
        color=label_col
    )
    fig.update_layout(
        xaxis_title="Warehouse / Location",
        yaxis_title="Inventory Quantity",
        showlegend=False
    )
    return fig