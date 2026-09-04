import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from configer import URLS
from fetcher import fetch_data


def build_orders_chart() -> go.Figure | None:
    """Order Status Breakdown by Year — stacked bar chart."""
    df = fetch_data(URLS["orders"])
    if df.empty:
        return None

    year_col   = next((c for c in df.columns if "year"   in c.lower()), df.columns[0])
    status_col = next((c for c in df.columns if "status" in c.lower()), df.columns[1])
    num_col    = df.select_dtypes(include=["number"]).columns
    num_col    = num_col[0] if len(num_col) > 0 else df.columns[-1]
    df[num_col] = pd.to_numeric(df[num_col], errors="coerce")

    fig = px.bar(
        df, x=year_col, y=num_col, color=status_col, barmode="stack",
        title="Order Status Breakdown by Year",
        color_discrete_map={
            "Shipped":   "#2ecc71",
            "Pending":   "#f39c12",
            "Cancelled": "#e74c3c"
        }
    )
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Number of Orders",
        hovermode="x unified"
    )
    return fig