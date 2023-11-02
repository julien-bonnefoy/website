import dash_bootstrap_components as dbc
from dash import dcc, html
from .functions import controls

content = dbc.Container(
    [
        html.H1("Iris k-means clustering", className="text-center"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls, md=4),
            ],
            align="center",
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="cluster-graph"), md=8)
            ],
            align="center",
        ),
    ],
    fluid=True,
)


def build_layout():
    return content
