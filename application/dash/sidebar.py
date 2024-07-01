import dash_bootstrap_components as dbc
from dash import html, dcc
import base64
from application.dash.biocodex.functions import df, join_id_adr_cdb, make_engine


def spe_slider(spe):
    df = join_id_adr_cdb(make_engine())
    sub_df = df[df["spe1"] == spe]
    return dbc.Row(
        [
            dbc.Col(
                [
                   spe
                ],
                style={"width": "40px"},
                width=1
            ),
            dbc.Col(
                [
                    dcc.RangeSlider(
                        sub_df.pvm.min(),
                        sub_df.pvm.max(),
                        id=f"{spe.lower()}-pvm-slider",
                        value = [sub_df.pvm.min(), sub_df.pvm.max()],
                        tooltip = {"placement": "bottom", "always_visible": True},
                        className="ms-1 w-100 px-0",
                        marks=None

                    )
                ],
                style={"transform": 'translateY(15px)', "flex-grow": "1"}
            )
        ],
        style={"display": "flex", "align-items": "center", "margin": "5%", "width":" 100%"}
    )


def options(df, col):
    return[{"label": value, "value": value} for value in df[col].unique()]

df = join_id_adr_cdb(make_engine())
df["nom_prenom"] = df["nom"] + ' ' + df["pre"]
noms_options = options(df.sort_values(by="nom"),"nom_prenom")
del df

FA = "https://use.fontawesome.com/releases/v5.15.1/css/all.css"
image_filename = "/var/www/website.julien-bonnefoy.dev/application/static/img/shield_125.png"

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

doctors_spes = {
    'GY': 'gynecologue',
    'MGY': 'medecin-generaliste',
    'SF': 'sage-femme',
    'MG': 'medecin-generaliste',
    'GE': 'gastro-enterologue',
    'PE': 'pediatre',
    'PPSY': 'pedopsychiatre',
    'PSY': 'psychiatre',
    'NE': 'neurologue'
}

spes_options = [{"label": spe.upper(), "value": spe} for spe in doctors_spes.keys()]

ciblage_options = [
    {"label": "HC", "value": 'HC'},
    {"label": "1", "value": 1},
    {"label": "2", "value": 2},
    {"label": "3", "value": 3},
    {"label": "4", "value": 4}
]

df = join_id_adr_cdb(make_engine())

sidebar_button = dbc.Button(
    [
        html.Span(
            [
                html.Span(className="hamburger-inner mt-0"),
            ],
            className="hamburger-box border-0"
        )
    ],
    id="sidebar-toggler",
    className="hamburger hamburger--elastic btn-dark",
)

sidebar_header = dbc.Row(
    [
        dbc.Col(
            [
                html.H1("FILTERS", )
            ],
            align="center"
        )
    ],
    justify="center",
    className="sidebar-header"
)

def build_sidebar(ugas=["75AUT"], spes=["GY", "MGY", "SF", "MG", "GE", "PE"], cib=[1, 2, 3, 4], pvm=[df.pvm.min(),df.pvm.max()]):

    return html.Div(
        [
            html.Div(
                [
                    sidebar_header,
                    dbc.Collapse(
                        [
                            html.Hr(),
                            dbc.Accordion(
                                [
                                    dbc.AccordionItem(
                                        [
                                            dcc.Dropdown(
                                                options=noms_options,

                                                id="noms-dd",
                                                maxHeight=300,
                                                searchable=True,
                                                clearable=True,
                                                style={"color": "black"}
                                            )
                                        ],
                                        title="NOMS",
                                    ),
                                    dbc.AccordionItem(
                                        [
                                            dcc.Checklist(
                                                options=uga_options,
                                                value=ugas,
                                                id="uga-cl",
                                                inline=True,
                                                inputStyle={"margin": "5px", "transform": "scale(1.25)"},
                                                labelStyle={"marginLeft": "5px"},
                                                inputClassName="col-3",
                                                labelClassName="col-3"
                                                #style={"display": "flex", "flex-wrap": "wrap", "justify-content": "space-evenly"}
                                            )
                                        ],
                                        title="UGA",
                                    ),
                                    dbc.AccordionItem(
                                        [
                                            dcc.Checklist(
                                                options=spes_options,
                                                value=spes,
                                                id="spe-cl",
                                                inline=True,
                                                inputStyle={"transform": "scale(1.25)"},
                                                labelStyle={"font-size": "12px"},
                                                labelClassName="col-4"
                                            )
                                        ],
                                        title="SPÉCIALITÉS"
                                    ),
                                    dbc.AccordionItem(
                                        [
                                            dcc.Checklist(
                                                options=ciblage_options,
                                                value=cib,
                                                id="cib-cl",
                                                inline=True,
                                                inputStyle={"margin": "5px", "transform": "scale(1.25)"},
                                                labelStyle={"marginLeft": "5px", "font-size": "12px"},
                                                style={"display": "flex", "flex-wrap": "wrap",
                                                       "justify-content": "space-evenly"}
                                            ),
                                        ],
                                        title="CIBLAGE",
                                    ),
                                    dbc.AccordionItem(
                                        [
                                            dcc.RangeSlider(
                                                df.pvm.min(),
                                                df.pvm.max(),
                                                id="pvm-slider",
                                                value=pvm,
                                                tooltip={"placement": "bottom", "always_visible": True},
                                                className="w-100"
                                            ),
                                        ],
                                        title="PVM",
                                    )
                            ],
                            always_open=True,
                            style={"font-size": "10px"},
                            active_item=["item-1", "item-2", "item-3"],
                                flush=True
                        )

                    ],
                    className="sidebar-content row",
                    is_open=True,

                )
            ]
        ),
        html.Div([sidebar_button], style={"height": "60px", "display": "flex", "justify-content": "end"}, id="hamburger-div")
    ],
    id="sidebar",
    className="collapsed",
    style={"padding": "0.9rem", "overflow-y": "scroll"}
)




