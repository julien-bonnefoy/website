import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash_extensions import Purify, DeferScript

dash.register_page(__name__, path='/calendar')

layout = html.Div(
    [
        html.Div(
            className="card card-calendar",
            style={"height": "100%"},
            children=[
                html.Div(
                    className="card-body p-3",
                    style={"max-height": "100%"},
                    children=[
                        html.Div(
                            id="calendar", **{"data-bs-toggle": "calendar"}
                        )
                    ]
                )
            ]
        ),
        DeferScript(src='assets/calendar.js'),
    ]
)