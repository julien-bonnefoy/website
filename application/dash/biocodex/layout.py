from dash import dcc, html
import dash_bootstrap_components as dbc
import dash
from application.dash.biocodex.functions import legend1, legend2
from application.dash.sidebar import sidebar
import visdcc
import dash_loading_spinners as dls


offcanvas = html.Div(
    [
        dbc.Offcanvas([

            html.Br(),
            dbc.Label("PVM", className="fw-bold"),
            legend1,
            html.Br(),
            dbc.Label("POTENTIEL", className="fw-bold"),
            legend2
        ],
            id="offcanvas",
            scrollable=True,
            title="FILTERS",
            is_open=False,
            placement='bottom',
            style={"height": "25%", "max-width": "100%"},
        )
    ]
)

def build_layout():
    return html.Div(
        [
            dcc.Store(id="memory"),
            visdcc.Run_js(id="visdcc"),
            sidebar,
            dbc.Row(
                [
                    html.Div(
                        [
                            dcc.Link(f"{page['name']}", href=page["relative_path"], className="btn btn-secondary w-100")
                        ], className="d-flex col-1"
                    ) for page in dash.page_registry.values()
                ]+[
                    html.Br(),
                    dash.page_container
                ],
                id="page-content",
                className="d-flex",
                justify="center"
            )
        ]
    )

