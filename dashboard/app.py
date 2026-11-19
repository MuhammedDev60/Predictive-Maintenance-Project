"""Wind turbine SCADA monitoring dashboard.

Input: data/processed/scada_clean.csv, created by Data.ipynb cell 17.
Run from the project root: python dashboard/app.py
"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "scada_clean.csv"

# Matches the status_types table defined in Data.ipynb.
STATUS_NAMES = {
    0: "Normal", 1: "Derated", 2: "Idling",
    3: "Service", 4: "Downtime", 5: "Other",
}
REQUIRED_COLUMNS = {
    "asset_id", "time_stamp", "status_type_id", "train_test",
    "wind_speed", "power_output", "gearbox_temp",
}


def load_data(path: Path) -> pd.DataFrame:
    if not path.is_file():
        raise FileNotFoundError(
            f"Cleaned dataset not found: {path}\n"
            "Run Data.ipynb through cell 17 first to export scada_clean.csv."
        )
    df = pd.read_csv(path, parse_dates=["time_stamp"])
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"Required columns missing from cleaned data: {sorted(missing)}")
    if df["time_stamp"].isna().any():
        raise ValueError("time_stamp contains invalid or missing dates.")
    df["status_name"] = df["status_type_id"].map(STATUS_NAMES).fillna("Unknown")
    return df


data = load_data(DATA_PATH)
minimum_date = data["time_stamp"].min().date()
maximum_date = data["time_stamp"].max().date()

assets = sorted(data["asset_id"].dropna().unique().tolist())
statuses = sorted(data["status_name"].dropna().unique().tolist())
splits = sorted(data["train_test"].dropna().unique().tolist())

app = Dash(__name__)
app.title = "Wind Turbine Performance Dashboard"

CARD = {
    "backgroundColor": "#ffffff", "padding": "18px", "borderRadius": "10px",
    "boxShadow": "0 1px 5px #d9e4e6", "minWidth": "170px", "flex": "1",
}


def kpi_card(title, component_id):
    return html.Div([
        html.Div(title, style={"fontSize": "13px", "color": "#52636d"}),
        html.H2(id=component_id, style={"margin": "8px 0 0"}),
    ], style=CARD)


app.layout = html.Div([
    html.H1("Wind Turbine Performance Monitoring"),
    html.P("Interactive exploration of cleaned Wind Farm A SCADA readings."),
    html.Div([
        html.Div([
            html.Label("Turbine(s)"),
            dcc.Dropdown(
                id="asset-filter",
                options=[{"label": str(a), "value": a} for a in assets],
                value=assets, multi=True,
            ),
        ], style={"flex": "1", "minWidth": "180px"}),
        html.Div([
            html.Label("Date range"),
            dcc.DatePickerRange(
                id="date-filter", min_date_allowed=minimum_date,
                max_date_allowed=maximum_date, start_date=minimum_date,
                end_date=maximum_date, display_format="YYYY-MM-DD",
            ),
        ], style={"flex": "1", "minWidth": "280px"}),
        html.Div([
            html.Label("Turbine status"),
            dcc.Dropdown(
                id="status-filter",
                options=[{"label": s, "value": s} for s in statuses],
                value=statuses, multi=True,
            ),
        ], style={"flex": "1", "minWidth": "180px"}),
        html.Div([
            html.Label("Data split"),
            dcc.Dropdown(
                id="split-filter",
                options=[{"label": s, "value": s} for s in splits],
                value=splits, multi=True,
            ),
        ], style={"flex": "1", "minWidth": "180px"}),
    ], style={"display": "flex", "gap": "18px", "flexWrap": "wrap", "marginBottom": "20px"}),
    html.Div(id="empty-message", style={"color": "#a33b33", "marginBottom": "10px"}),
    html.Div([
        kpi_card("SCADA readings", "readings-kpi"),
        kpi_card("Turbines", "turbines-kpi"),
        kpi_card("Average power output (source units)", "power-kpi"),
        kpi_card("Average wind speed (source units)", "wind-kpi"),
        kpi_card("Average gearbox temperature (source units)", "gearbox-kpi"),
    ], style={"display": "flex", "flexWrap": "wrap", "gap": "12px"}),
    html.Div([
        dcc.Graph(id="power-trend"),
        dcc.Graph(id="asset-power"),
        dcc.Graph(id="status-distribution"),
        dcc.Graph(id="wind-band-power"),
    ], style={"display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(360px, 1fr))"}),
    html.P(
        "KPIs summarize filtered SCADA rows, not unique failure events or energy generated. "
        "Measurement units are not assumed because the notebook's data dictionary does not specify them.",
        style={"fontSize": "12px", "color": "#52636d"},
    ),
], style={
    "backgroundColor": "#f2f6f7", "padding": "24px", "minHeight": "100vh",
    "fontFamily": "Arial, sans-serif", "color": "#18323b",
})


def blank_chart(title):
    fig = px.scatter(title=title)
    fig.update_layout(annotations=[dict(
        text="No data for the selected filters", x=0.5, y=0.5,
        xref="paper", yref="paper", showarrow=False,
    )])
    return fig


@app.callback(
    Output("readings-kpi", "children"),
    Output("turbines-kpi", "children"),
    Output("power-kpi", "children"),
    Output("wind-kpi", "children"),
    Output("gearbox-kpi", "children"),
    Output("power-trend", "figure"),
    Output("asset-power", "figure"),
    Output("status-distribution", "figure"),
    Output("wind-band-power", "figure"),
    Output("empty-message", "children"),
    Input("asset-filter", "value"),
    Input("date-filter", "start_date"),
    Input("date-filter", "end_date"),
    Input("status-filter", "value"),
    Input("split-filter", "value"),
)
def update_dashboard(selected_assets, start_date, end_date, selected_statuses, selected_splits):
    selected_assets = selected_assets or []
    selected_statuses = selected_statuses or []
    selected_splits = selected_splits or []
    if not start_date or not end_date:
        filtered = data.iloc[0:0]
    else:
        # Inclusive end date, regardless of the reading's time of day.
        start = pd.Timestamp(start_date).normalize()
        end_exclusive = pd.Timestamp(end_date).normalize() + pd.Timedelta(days=1)
        filtered = data.loc[
            data["asset_id"].isin(selected_assets)
            & data["status_name"].isin(selected_statuses)
            & data["train_test"].isin(selected_splits)
            & data["time_stamp"].ge(start)
            & data["time_stamp"].lt(end_exclusive)
        ]

    if filtered.empty:
        titles = ["Average power by month", "Average power by turbine",
                  "SCADA readings by status", "Average power by wind-speed band"]
        return ("0", "0", "N/A", "N/A", "N/A",
                *(blank_chart(t) for t in titles),
                "No readings match the selected filters.")

    monthly = (filtered.assign(month=filtered["time_stamp"].dt.to_period("M").dt.to_timestamp())
               .groupby("month", as_index=False)["power_output"].mean())
    trend = px.line(monthly, x="month", y="power_output",
                    markers=True, title="Average power by month",
                    labels={"month": "Month", "power_output": "Average power (source units)"})

    by_asset = filtered.groupby("asset_id", as_index=False)["power_output"].mean()
    by_asset["asset_id"] = by_asset["asset_id"].astype(str)
    asset_chart = px.bar(by_asset, x="asset_id", y="power_output",
                         title="Average power by turbine",
                         labels={"asset_id": "Turbine ID", "power_output": "Average power (source units)"})

    by_status = filtered.groupby("status_name", as_index=False).size()
    status_chart = px.pie(by_status, names="status_name", values="size",
                          title="SCADA readings by status")

    # Same 4/10 wind-speed thresholds used in notebook SQL query 7.
    wind_bands = filtered.assign(wind_band=np.select(
        [filtered["wind_speed"] < 4, filtered["wind_speed"] <= 10],
        ["Low Wind", "Medium Wind"], default="High Wind",
    ))
    band_summary = (wind_bands.groupby("wind_band", observed=True, as_index=False)
                    ["power_output"].mean())
    wind_chart = px.bar(band_summary, x="wind_band", y="power_output",
                        title="Average power by wind-speed band",
                        labels={"wind_band": "Wind-speed band", "power_output": "Average power (source units)"})

    return (
        f"{len(filtered):,}",
        f"{filtered['asset_id'].nunique():,}",
        f"{filtered['power_output'].mean():,.2f}",
        f"{filtered['wind_speed'].mean():,.2f}",
        f"{filtered['gearbox_temp'].mean():,.2f}",
        trend, asset_chart, status_chart, wind_chart, "",
    )


if __name__ == "__main__":
    app.run(debug=False)
