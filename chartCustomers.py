import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from configer import URLS
from fetcher import fetch_data


def build_customers_chart() -> go.Figure | None:
    """Top Customers by Total Spend — horizontal bar chart."""
    df = fetch_data(URLS["customers"])
    if df.empty:
        return None

    cust_col = next(
        (c for c in df.columns if "customer" in c.lower() or "name" in c.lower()),
        df.columns[0]
    )
    spend_col = df.select_dtypes(include=["number"]).columns
    spend_col = spend_col[0] if len(spend_col) > 0 else df.columns[-1]
    df[spend_col] = pd.to_numeric(df[spend_col], errors="coerce")

    fig = px.bar(
        df.head(15), x=spend_col, y=cust_col, orientation="h",
        title="Top Customers by Total Spend",
        color=spend_col, color_continuous_scale="Blues"
    )
    fig.update_layout(
        xaxis_title="Total Spend",
        yaxis_title="Customer",
        yaxis={"categoryorder": "total ascending"},
        showlegend=False
    )
    return fig