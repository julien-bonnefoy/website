from ....data.orange_data import df
from ..functions import make_counter_row, make_footer, make_dd, make_cloud, make_histo
from dash_daq.ToggleSwitch import ToggleSwitch
from dash_daq.GraduatedBar import GraduatedBar
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from .textes import p_8


col_1 = "supplier"
col_2 = "lo_id"
name_1 = "fournisseurs "
name_2 = "learning objects "
n = 10
supp_counter = make_counter_row(df, col_1, name_1)
supp_dd = make_dd(df, col_1)
supp_cloud = make_cloud(df, col_1, "dash", True)
graph = make_histo(df, col_1, n)

content = dbc.Container(
    [
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Img(
                                    src=supp_cloud,
                                    id="supplier_wc_img",
                                    className="img-responsive",
                                    width="100%",
                                    height="100%"
                                )
                            ],
                            className="d-flex align-items-center justify-content-center",
                            style={"border-right": "2px solid #ff7900"}
                        ),
                        dbc.Col(
                            [
                                supp_counter,
                                html.Div(
                                    [
                                    ],
                                    id="lo_id_counter_row"
                                ),
                                dbc.Row(
                                    [
                                        html.P(
                                            "Pour afficher les données d'un fournisseur, sélectionnez "
                                            "dans la liste ci-dessous oo cliquez sur une barre de l'histogramme "
                                            "qui suit.",
                                            style={"text-align": "center"}
                                        )
                                    ],
                                    id="instructions",
                                    className="d-flex align-items-end justify-content-center",
                                    style={"height": "25%"}
                                ),
                                dbc.Row(
                                    [
                                        supp_dd
                                    ],
                                    className="h-25 align-items-center align-items-start mb-1"
                                )
                            ]
                        ),
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardHeader(
                                            [
                                                html.H5(
                                                    [
                                                        "TOP 10 ",
                                                        html.Sup(
                                                            [
                                                                html.I(className="fa fa-info-circle")
                                                            ],
                                                            id="top-10-tooltip"
                                                        )
                                                    ],
                                                    style={
                                                        "marginBottom": 0,
                                                        "color": "#000"
                                                    },
                                                ),
                                                dbc.Tooltip(
                                                    [
                                                        "en nombre de Learning Objects par Fournisseur."
                                                    ],
                                                    delay={"hide": 1000},
                                                    target="top-10-tooltip",
                                                    placement="top"
                                                )
                                            ],
                                            style={"backgroundColor": "#fff"},
                                            className="d-flex justify-content-center border-0"
                                        ),
                                        dcc.Loading(
                                            [
                                                dcc.Graph(
                                                    figure=graph,
                                                    id="supplier_histo",
                                                    config={'displayModeBar': False},
                                                    className="",
                                                    style={"height": "21vh"}
                                                )
                                            ],
                                            id="supplier_loader",
                                            type="cube",
                                            color="#ff7900"
                                        ),
                                        make_footer("Survolez les barres pour découvrir les fournisseurs")
                                    ],
                                    className="h-100 border-0"
                                )
                            ],
                            className="d-flex flex-column",
                            style={"border-left": "2px solid #000"}
                        )
                    ],
                    id="filter_row",
                    className="row-cols-1 row-cols-sm-1 row-cols-md-1 row-cols-lg-3 row-cols-xl-3 mt-2 mb-2 w-100",
                )
            ]
        ),
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardHeader(
                                            [
                                                html.H1(
                                                    [
                                                        "TYPES & STATUTS",
                                                    ],
                                                    style={
                                                        "marginBottom": 0,
                                                        "fontSize": "3vmin",
                                                        "color": "#000"
                                                    },
                                                )
                                            ],
                                            style={"backgroundColor": "#fff"},
                                            className="d-flex justify-content-center border-1"
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        ToggleSwitch(
                                                            id="view_switch",
                                                            label=['Vue combinée'.upper(), 'Vue séparée'.upper()],
                                                            color="#ff7900",
                                                            value="Vue séparée"
                                                        )
                                                    ],
                                                    id="view_switch_col",
                                                    width={"size": 6, "offset": 3},
                                                    className=""
                                                )
                                            ],
                                            className="mt-1"
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        dbc.Button(
                                                            [html.Span(className="fa fa-question-circle fa-3x")],
                                                            id="sun-modal-button",
                                                            className="border-0",
                                                            block=True,
                                                            style={"font-size": "1vmin"}
                                                        ),
                                                        dbc.Modal(
                                                            [
                                                                dbc.ModalHeader("VUES"),
                                                                dbc.ModalBody([p_8]),
                                                                dbc.ModalFooter(
                                                                    dbc.Button("Close", id="sun-modal-close",
                                                                               className="ml-auto")
                                                                ),
                                                            ],
                                                            id="sun-modal",
                                                            centered=True,
                                                        )
                                                    ],
                                                    width={"size": 4, "offset": 4}
                                                )
                                            ],
                                            className="mt-1 ml-1"
                                        ),
                                        dbc.CardBody(
                                            [
                                                dbc.Col(
                                                    [
                                                        dbc.Row(
                                                            [
                                                                dcc.Loading(
                                                                    [
                                                                        dcc.Graph(
                                                                            id="active_status_lo_type_sun",
                                                                            config={'displayModeBar': False},
                                                                            style={"height": "33vh",
                                                                                   "max-width": "23vw"},
                                                                            className="py-3"
                                                                        )
                                                                    ],
                                                                    color="#ff7900",
                                                                    id="active_status_lo_type_sun_loader"
                                                                )
                                                            ],
                                                            id="active_status_lo_type_sun_body",
                                                            className="d-flex justify-content-center align-items-center"
                                                        )
                                                    ],
                                                    id="active_status_lo_type_sun_col",
                                                    # width=5,
                                                    className="d-flex flex-column justify-content-center align-items-center"
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Row(
                                                            [
                                                                dcc.Loading(
                                                                    [
                                                                        dcc.Graph(
                                                                            id="lo_type_pie",
                                                                            config={'displayModeBar': False},
                                                                            style={"height": "25vh",
                                                                                   "max-width": "20vw"},
                                                                            className="py-3"
                                                                        )
                                                                    ],
                                                                    color="#ff7900",
                                                                    id="lo_type_pie_loader"
                                                                )
                                                            ],
                                                            id="lo_type_pie_body",
                                                            className="d-flex justify-content-center align-items-center"
                                                        )
                                                    ],
                                                    id="lo_type_pie_col",
                                                    width=6
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Row(
                                                            [
                                                                dcc.Loading(
                                                                    [
                                                                        dcc.Graph(
                                                                            id="active_status_pie",
                                                                            config={'displayModeBar': False},
                                                                            style={"height": "25vh",
                                                                                   "max-width": "20vw"},
                                                                            className="py-3"
                                                                        )
                                                                    ],
                                                                    color="#ff7900",
                                                                    id="active_status_pie_loader"
                                                                )
                                                            ],
                                                            id="active_status_pie_body",
                                                            className="d-flex justify-content-center align-items-center"
                                                        )
                                                    ],
                                                    id="active_status_pie_col",
                                                    width=6
                                                )
                                            ],
                                            className="d-flex align-items-center justify-content-center py-0"
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        ToggleSwitch(
                                                            id="order_switch",
                                                            label=['TYPE >>> STATUT', 'STATUT >>> TYPE'],
                                                            color="#ff7900"
                                                        )
                                                    ],
                                                    id="order_switch_col",
                                                    width={"size": 6, "offset": 3},
                                                    className="d-flex flex-column justify-content-center align-items-center"
                                                )
                                            ]
                                        )
                                    ],
                                    className="h-100 border-0"
                                )
                            ],
                            width={"size": 6, "offset": ""},
                        ),
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardHeader(
                                            [
                                                html.H1(
                                                    [
                                                        "catégories".upper()
                                                    ],
                                                    style={
                                                        "marginBottom": 0,
                                                        "fontSize": "3vmin",
                                                        "color": "#000"
                                                    },
                                                )
                                            ],
                                            className="d-flex w-100 justify-content-center border-1",
                                            style={
                                                "backgroundColor": "#fff"
                                            }
                                        ),
                                        dbc.Row(
                                            [
                                                html.H1(
                                                    [
                                                    ],
                                                    id="subject_missing_bar_title",
                                                    style={"color": "#ff7900", "font-size": "2.75vmin"}
                                                )
                                            ],
                                            className="d-flex justify-content-center mt-0 mb-2 mx-4 w-100",
                                        ),
                                        dbc.Row(
                                            [
                                                GraduatedBar(
                                                    id="subject_missing_bar",
                                                    color={
                                                        "gradient": True,
                                                        "ranges": {
                                                            "red": [0, 4],
                                                            "yellow": [4, 8],
                                                            "green": [8, 10]}},
                                                    max=10,
                                                    min=0,
                                                    size=150,
                                                )
                                            ],
                                            className="d-flex justify-content-center mt-0 mb-2 mx-4 w-100"
                                        ),
                                        dbc.CardBody(
                                            [
                                                dbc.Col(
                                                    [
                                                        dbc.Row(
                                                            [
                                                                dcc.Loading(
                                                                    [
                                                                        dcc.Graph(
                                                                            id="subject_pie",
                                                                            config={'displayModeBar': False},
                                                                            style={"height": "33vh",
                                                                                   "max-width": "23vw"},
                                                                            className="py-3"
                                                                        )
                                                                    ],
                                                                    color="#ff7900",
                                                                    id="subject_pie_loader"
                                                                )
                                                            ],
                                                            id="subject_pie_body",
                                                            className="d-flex justify-content-center align-items-center"
                                                        )
                                                    ],
                                                    width=12,
                                                    className=""
                                                )
                                            ],
                                            className="d-flex py-0 align-items-center justify-content-center"
                                        )
                                    ],
                                    className="d-flex w-100 border-0"
                                )
                            ],
                            # width={"size": 6, "offset": 1},
                            className="d-flex justify-content-center px-0 border-0"
                        )
                    ],
                    className="row-cols-1 row-cols-sm-1 row-cols-md-2 row-cols-lg-2 row-cols-xl-2 mt-2 mb-2 w-100",
                )
            ]
        )
    ],
    fluid=True,
    className="d-flex flex-column mx-0",
    style={"max-width": "100%"}
)


