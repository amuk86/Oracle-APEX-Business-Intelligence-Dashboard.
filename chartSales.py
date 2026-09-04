import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from configer import URLS
from fetcher import fetch_data


def build_sales_chart() -> go.Figure | None:
    """Monthly Sales Trend — line chart with markers."""
    df = fetch_data(URLS["sales"])
    if df.empty:
        return None

    date_col  = df.select_dtypes(exclude=["number"]).columns[0]
    sales_col = df.select_dtypes(include=["number"]).columns
    sales_col = sales_col[0] if len(sales_col) > 0 else df.columns[-1]
    df[sales_col] = pd.to_numeric(df[sales_col], errors="coerce")

    fig = px.line(
        df, x=date_col, y=sales_col,
        title="Monthly Sales Trend",
        markers=True
    )
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Sales Amount"
    )
    return fig