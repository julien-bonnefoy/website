import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from .functions import controls

content = dbc.Container(
    [
        html.H1("Iris k-means clustering"),
        html.Hr(),
        dbc.Row(
            [dbc.Col(controls, md=4), dbc.Col(dcc.Graph(id="cluster-graph"), md=8),],
            align="center",
        ),
    ],
    fluid=True,
)


def build_layout():
    return content
