from dash import html, callback, Input, Output, State
import dash
import dash_loading_spinners as dls

dash.register_page(__name__, path="/tiles")

layout = dls.Hash(
    [
        html.Div(id="tiles-content", className="d-flex flex-row flex-wrap justify-content-space-evenly")
    ],
    color='#000080',
    debounce=1000,
    size=100,
)