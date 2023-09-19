import dash_bootstrap_components as dbc
from dash import html, dcc
from .biocodex.functions import uga_options, spe_options, ciblage_options
import base64

FA = "https://use.fontawesome.com/releases/v5.15.1/css/all.css"
image_filename = "application/static/img/shield_125.png"

encoded_image = base64.b64encode(open(image_filename, 'rb').read())

sidebar_buttons = dbc.Row(
    [
        dbc.Col(
            [
                dbc.Button(
                    [
                        html.Span(
                            [
                                html.Span(className="hamburger-inner"),
                            ],
                            className="hamburger-box border-0"
                        )
                    ],
                    id="sidebar-toggle",
                    className="hamburger is-active border-0",
                ),
                dbc.Button(
                    [
                        html.Span(
                            [
                                html.Span(className="hamburger-inner"),
                            ],
                            className="hamburger-box"
                        )
                    ],
                    id="navbar-toggle",
                    className="hamburger is-active",
                )
            ],
            className="d-flex flex-row-reverse border-0"
        )
    ]
)

sidebar_header = dbc.Row(
    [
        dbc.Col(
            [
                # width: 3rem ensures the logo is the exact width of the
                # collapsed sidebar (accounting for padding)
                html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), className="d-flex w-25"),
            ]
        )
    ],
    className="sidebar-header"
)

sidebar1 = html.Div(
    [
        sidebar_buttons,
        sidebar_header,
        dbc.Collapse(
            [
                html.Hr(),
                dbc.Label("SPÉCIALITÉS", className="fw-bold"),
                dcc.Checklist(
                    options=spe_options,
                    value=[spe_options[3]["value"]],
                    id="spe-check",
                    inline=True,
                    inputStyle={"margin-right": "5px"},
                    labelStyle={"margin-right": "5px"}
                ),
                html.Br(),
                dbc.Label("UGA", className="fw-bold"),
                dcc.Checklist(
                    options=uga_options,
                    value=[uga_options[i]["value"] for i in range(len(uga_options))],
                    id="uga-check",
                    inline=True,
                    inputStyle={"margin-right": "5px"},
                    labelStyle={"margin-right": "5px"}
                ),
                html.Br(),
                dbc.Label("CIBLAGE", className="fw-bold"),
                dcc.Checklist(
                    options=ciblage_options,
                    value=[ciblage_options[i]["value"] for i in range(len(ciblage_options))],
                    id="ciblage-check",
                    inline=True,
                    inputStyle={"margin-right": "5px"},
                    labelStyle={"margin-right": "5px"}
                ),
            ],
            id="sidebar-body-collapse"
        )
    ],
    id="sidebar",
    className="collapsed"
)

sidebar2 = html.Div(
    [
        sidebar_buttons,
        sidebar_header,
        dbc.Collapse(
            [
                html.Hr(),
                dbc.Label("UGA", className="fw-bold"),
                dcc.Checklist(
                    options=uga_options,
                    value=[uga_options[i]["value"] for i in range(len(uga_options))],
                    id="uga-check",
                    inline=True,
                    inputStyle={"margin-right": "5px"},
                    labelStyle={"margin-right": "5px"}
                )
            ],
            id="sidebar-body-collapse"
        )
    ],
    id="sidebar",
    className="collapsed"
)

def build_sidebar():
    return sidebar


