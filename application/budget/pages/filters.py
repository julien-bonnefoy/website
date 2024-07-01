from dash import dcc
import dash_bootstrap_components as dbc
from ..helpers.styles import CARD_STYLE
import pandas as pd


statement_dir = "/home/julien/Documents/Finances/Banque/Lydia/bankstatement"
csv_fn = f"{statement_dir}/csv/compile.csv"
df = pd.read_csv(csv_fn, sep=";", keep_default_na=False, parse_dates=['date_dt'], dayfirst=True)
daterange = pd.date_range(start=df["date_dt"].min(), end=df["date_dt"].max(), freq='M')
months = list(df['year_mth'].unique())
months.sort()

ddowns_col = dbc.Col(
    [
        dbc.Card(
            [
                dbc.Label("CATEGORIES"),
                dcc.Dropdown(
                    id='category-dd',
                    options=[{"label": cat, "value": cat} for cat in list(df["category"].unique())],
                    value=None,
                    placeholder="Select category",
                    multi=True
                ),
                dbc.Label("MONTH"),
                dcc.Dropdown(
                    id='months-dd',
                    options=[{"label": pd.to_datetime(month, format="%Y %m").strftime("%B %Y"), "value": month} for
                             month in list(df["year_mth"].unique())],
                    placeholder="Select months",
                    multi=True
                )
            ],
            class_name="text-center",
            style=CARD_STYLE,
            body=True,
        )
    ]
)