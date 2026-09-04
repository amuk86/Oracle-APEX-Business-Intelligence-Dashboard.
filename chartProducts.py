import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from configer import URLS
from fetcher import fetch_data


def build_products_chart() -> go.Figure | None:
    """Top Products by Total Revenue — horizontal bar chart."""
    df = fetch_data(URLS["products"])
    if df.empty:
        return None

    prod_col = next(
        (c for c in df.columns if "product" in c.lower() or "name" in c.lower()),
        df.columns[0]
    )
    rev_col = df.select_dtypes(include=["number"]).columns
    rev_col = rev_col[0] if len(rev_col) > 0 else df.columns[-1]
    df[rev_col] = pd.to_numeric(df[rev_col], errors="coerce")

    fig = px.bar(
        df.head(20), x=rev_col, y=prod_col, orientation="h",
        title="Top Products by Total Revenue",
        color=rev_col, color_continuous_scale="Viridis"
    )
    fig.update_layout(
        xaxis_title="Total Revenue",
        yaxis_title="Product",
        yaxis={"categoryorder": "total ascending"},
        showlegend=False
    )
    return fig