from dash import dcc, html
import dash_bootstrap_components as dbc
import dash
from application.dash.sidebar import build_sidebar
import visdcc
from application.dash.biocodex.functions import join_id_adr_cdb


def build_layout():
    return html.Div(
        [
            dcc.Store(id="all-memory", data=join_id_adr_cdb().to_dict('records')),
            visdcc.Run_js(id="visdcc"),
            build_sidebar(),
            html.Div(
                [
                    dcc.Store(id="memory"),
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    html.A(f"{page['name']}", href=page["relative_path"],
                                             className="btn btn-secondary w-100", id=f"link2-{page['name'].lower()}")
                                ], className="d-flex col-1 mx-2"
                            ) for page in dash.page_registry.values()
                        ],
                        className="d-flex flex-row mt-2",
                        style={"justify-content": "center"}
                    ),
                    html.Br(),
                    dbc.Col([dash.page_container], id="page-container", className="d-flex h-100 w-100 justify-content-center")
                ],
                id="dash-page"
            )
        ],
        id="page-content",
        className="h-100",
    )

