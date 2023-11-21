from dash import dcc, html
import dash_bootstrap_components as dbc
import dash
from application.dash.sidebar import build_sidebar
import visdcc
import dash_loading_spinners as dls


def build_layout():
    return html.Div(
        [
            dcc.Store(id="memory"),
            visdcc.Run_js(id="visdcc"),
            build_sidebar(),
            html.Div(
                [

                    dbc.Col(
                        [
                            html.Div(
                                [
                                    dcc.Link(f"{page['name']}", href=page["relative_path"],
                                             className="btn btn-secondary w-100")
                                ], className="d-flex col-1 mx-2"
                            ) for page in dash.page_registry.values()
                        ],
                        className="d-flex flex-row mt-2",
                        style={"justify-content": "center"}
                    ),
                    html.Br(),
                    dbc.Col([dash.page_container], id="page-container", className="d-flex h-100 w-100")
                ],
                id="dash-page"
            )
        ],
        id="page-content",
        className="h-100",
    )

