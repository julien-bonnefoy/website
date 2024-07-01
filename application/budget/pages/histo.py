from dash import dcc
import dash
dash.register_page(__name__, path="/histo")

layout = dash.html.Div(
    [
        dcc.Graph(
            id="graph-content"
        )
    ]
)