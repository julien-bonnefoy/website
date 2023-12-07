import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/calendar')

layout = dbc.Row(
    [
        dbc.Col(id="calendar", className="mx-auto", style={"max-width": "75%"})
    ],
    className="d-flex",
    justify="center"

)