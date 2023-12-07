import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/')

layout = dbc.Row(
    [
        dbc.Col([html.H1('Dash Biocodex Home page')], width=6)
    ],
    className="d-flex",
    justify="center"
)