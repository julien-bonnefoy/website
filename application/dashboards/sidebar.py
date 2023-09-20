import dash_bootstrap_components as dbc
from dash import html, dcc
import base64
from random import randint

FA = "https://use.fontawesome.com/releases/v5.15.1/css/all.css"
image_filename = "application/static/img/shield_125.png"

encoded_image = base64.b64encode(open(image_filename, 'rb').read())


uga_options = [
    {'label': '75AUT', 'value': '75AUT'},
    {'label': '75ELY', 'value': '75ELY'},
    {'label': '75GRE', 'value': '75GRE'},
    {'label': '75INV', 'value': '75INV'},
    {'label': '75MNP', 'value': '75MNP'},
    {'label': '75PAS', 'value': '75PAS'},
    {'label': '75PER', 'value': '75PER'},
    {'label': '75TER', 'value': '75TER'},
    {'label': '75TRO', 'value': '75TRO'},
    {'label': '75VAU', 'value': '75VAU'},
    {'label': '92LEV', 'value': '92LEV'},
    {'label': '92NEU', 'value': '92NEU'}
]

spe_options = [
    {'label': 'GY', 'value': 'GY'},
    {'label': 'MG-GY', 'value': 'MG-GY'},
    {'label': 'SF', 'value': 'SF'},
    {'label': 'MG', 'value': 'MG'},
    {'label': 'GE', 'value': 'GE'},
    {'label': 'PE', 'value': 'PE'},
    {'label': 'PE-PSY', 'value': 'PE-PSY'},
    {'label': 'PSY', 'value': 'PSY'},
    {'label': 'NE', 'value': 'NE'},
]

ciblage_options = [
    {"label": "Non ciblé", "value": 0},
    {"label": "1", "value": 1},
    {"label": "2", "value": 2},
    {"label": "3", "value": 3},
    {"label": "4", "value": 4}
]


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
                    id="spe-cl",
                    inline=True,
                    inputStyle={"margin-right": "5px"},
                    labelStyle={"margin-right": "5px"}
                ),
                html.Br(),
                dbc.Label("UGA", className="fw-bold"),
                dcc.Checklist(
                    options=uga_options,
                    value=[uga_options[i]["value"] for i in range(len(uga_options))],
                    id="uga-cl",
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
                    value=[uga_options[randint(0,len(uga_options)-1)]["value"]],
                    id="uga-cl",
                    inline=True,
                    inputStyle={"margin-right": "5px"},
                    labelStyle={"margin-right": "5px"}
                ),
                html.Hr(),
                dbc.Label("SPÉCIALITÉS", className="fw-bold"),
                dcc.Checklist(
                    options=spe_options,
                    value=[spe_options[3]["value"]],
                    id="spe-cl",
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



