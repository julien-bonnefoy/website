from dash import html
import dash

dash.register_page(__name__, path="/tiles")


layout = html.Div(
[
    html.Div(
        [],
            id="tiles-content",
            className="w-100 flex-row flex-wrap container-fluid p-0 m-0 align-items-baseline justify-content-center d-flex",
            # style={"align-content": "baseline"}
        )
    ],
    style={"color": "#000080", "height": "100%"},
    className="d-flex"
)