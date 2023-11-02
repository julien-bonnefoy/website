import dash_bootstrap_components as dbc
from dash import html, dcc
import base64
from application.dash.biocodex.functions import data_df, join_id_adr_cdb


def options(df, col):
    return[{"label": value, "value": value} for value in df[col].unique()]

df = join_id_adr_cdb()
df["nom_prenom"] = df["nom"] + ' ' + df["prenom"]
noms_options = options(df, "nom_prenom")
del df

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

doctors_spes = {
    'GY': 'gynecologue',
    'MG-GY': 'medecin-generaliste',
    'SF': 'sage-femme',
    'MG': 'medecin-generaliste',
    'GE': 'gastro-enterologue',
    'PE': 'pediatre',
    'PE-PSY': 'pedopsychiatre',
    'PSY': 'psychiatre',
    'NE': 'neurologue'
}

doctors_features = {}

spes_options = [{"label": spe, "value": spe} for spe in doctors_spes.keys()]

ciblage_options = [
    {"label": "HC", "value": 'HC'},
    {"label": "1", "value": 1},
    {"label": "2", "value": 2},
    {"label": "3", "value": 3},
    {"label": "4", "value": 4}
]

for spe in doctors_spes.keys():
    sub_df = data_df[data_df["spe"] == spe]
    doctors_features[spe] = {
        'special': doctors_spes[spe],
        'slider': dcc.RangeSlider(sub_df.pot.min(), sub_df.pot.max(), id=f"{spe}-pot-slider",  value = [sub_df.pot.min(), sub_df.pot.max()], tooltip = {"placement": "bottom", "always_visible": True})
    }



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

sidebar = html.Div(
    [
        sidebar_header,
        dbc.Collapse(
            [
                html.Hr(),
                dbc.Label("NOMS", className="text-center fw-bold"),
                dcc.Dropdown(
                    options=noms_options,
                    id="noms-dd",
                    maxHeight=300,
                    searchable=True,
                    clearable=True,
                    style={"color": "black"}
                ),
                html.Hr(),
                dbc.Label("UGA", className="text-center fw-bold"),
                dcc.Checklist(
                    options=uga_options,
                    value=["75AUT"],
                    id="uga-cl",
                    inline=True,
                    inputStyle={"marginRight": "5px"},
                    labelStyle={"marginRight": "5px"}
                ),
                html.Hr(),
                dbc.Label("SPÉCIALITÉS", className="text-center fw-bold"),
                dcc.Checklist(
                    options=spes_options,
                    value=["GY", "MG-GY", "SF", "MG", "GE", "PE"],
                    id="spe-cl",
                    inline=True,
                    inputStyle={"marginRight": "5px"},
                    labelStyle={"marginRight": "5px"}
                ),
                html.Hr(),
                dbc.Label("CIBLAGE", className="text-center fw-bold"),
                dcc.Checklist(
                    options=ciblage_options,
                    value=[1, 2, 3, 4],
                    id="cib-cl",
                    inline=True,
                    inputStyle={"marginRight": "5px"},
                    labelStyle={"marginRight": "5px"}
                ),
                html.Hr(),
                dbc.Label("PVM", className="text-center fw-bold"),
                dcc.RangeSlider(
                    data_df.pvm.min(),
                    data_df.pvm.max(),
                    id="pvm-slider",
                    value=[data_df.pvm.min(),data_df.pvm.max()],
                    tooltip={"placement": "bottom", "always_visible": True},
                    className="w-100"
                ),
            ],
            className="sidebar-content",
            is_open=True
        ),
        sidebar_button,
    ],
    id="sidebar",
    className="collapsed",
    style={"padding": "0.9rem"}
)



