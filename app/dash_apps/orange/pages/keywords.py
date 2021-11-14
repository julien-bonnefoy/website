import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash_daq.Knob import Knob
from dash_daq.BooleanSwitch import BooleanSwitch
from dash_daq.LEDDisplay import LEDDisplay
from dash_table import DataTable
from .textes import p_6, p_7
from ....data.orange_data import df


dd_col = dbc.Col(
    [
        dcc.Dropdown(
            id="supplier_drop",
            options=[
                {"label": name, "value": name} for name in df["supplier"].dropna().unique()
            ],
            style={
                "width": "100%"
            }
        )
    ],
    className="w-100 px-0",
    width={"size": 3, "offset": 0}
)

title_col = dbc.Col(
    [
        html.H5(
            [
                "Sélectionnez un fournisseur pour affiner les résultats"
            ]
        )
    ],
    className="d-flex text-center",
    width={"size": 3, "offset": 3}
)

content = dbc.Container(
    [
        dbc.Row(
            [
                title_col, dd_col,
            ],
            className="d-flex align-items-center mt-4 w-100"
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        dbc.Button(
                                                            [
                                                                html.Span(className="fa fa-chevron-circle-down fa-2x")
                                                            ],
                                                            id="freq-header-expand-btn",
                                                            color="dark",
                                                            size="sm",
                                                            block=True,
                                                            className="h-100"
                                                        )
                                                    ],
                                                    width={'size': 1},
                                                    style={'text-align': 'center'}
                                                ),
                                                dbc.Col(
                                                    [
                                                        html.H5(
                                                            [
                                                                "MOTS FRÉQUENTS ET MOTS CLÉS ",
                                                                html.Span(id="freq_tooltip", className="fa fa-info-circle")
                                                            ],
                                                            style={
                                                                "color": "#ff7900",
                                                                "font-weight": "900",
                                                                "margin-bottom": "0"
                                                            }
                                                        )
                                                    ],
                                                    width={'size': 10},
                                                    style={'text-align': 'center'}
                                                ),
                                                dbc.Tooltip(
                                                    [
                                                        p_6
                                                    ],
                                                    target="freq_tooltip",
                                                    placement="right"
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Button(
                                                            [
                                                                html.Span(className="fa fa-chevron-circle-up fa-2x")
                                                            ],
                                                            id="freq-header-collapse-btn",
                                                            color="dark",
                                                            size="sm",
                                                            block=True,
                                                            className="h-100"
                                                        )
                                                    ],
                                                    width={'size': 1},
                                                    style={'text-align': 'center'}
                                                )
                                            ]
                                        )
                                    ],
                                    style={"color": "#000", "background-color": "#fff"},
                                    className="border-0"
                                ),
                                dbc.Collapse(
                                    [
                                        dbc.CardBody(
                                            [
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            [
                                                                dbc.Row(
                                                                    [
                                                                        dcc.Loading(
                                                                            [
                                                                                html.Img(
                                                                                    id="kw_cloud",
                                                                                    className="img-responsive",
                                                                                    width='100%',
                                                                                    style={
                                                                                        "transform": "scaleY(1.5)"
                                                                                    }
                                                                                )
                                                                            ],
                                                                            type="circle",
                                                                            color="#ff7900"
                                                                        )
                                                                    ],
                                                                    className=""
                                                                )
                                                            ],
                                                            width=4,
                                                            className="d-flex justify-content-center align-items-center"
                                                        ),
                                                        dbc.Col(
                                                            [
                                                                html.H6(
                                                                    "Sélectionnez le nombre de mots les plus "
                                                                    "fréquents que vous souhaitez retirer du "
                                                                    "vocabulaire"),
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(
                                                                            [
                                                                                Knob(
                                                                                    id="knob",
                                                                                    color='#ff7900',
                                                                                    size=100,
                                                                                    max=50,
                                                                                    value=0,
                                                                                    scale={'start': 0, 'labelInterval': 2, 'interval': 5}
                                                                                ),
                                                                            ]
                                                                        ),
                                                                        dbc.Col(
                                                                            [
                                                                                BooleanSwitch(id="switch_knob", on=False, color='#ff7900'),
                                                                                html.H6("Proceed")
                                                                            ],
                                                                            align='center'
                                                                        )
                                                                    ],
                                                                    className="justify-content-center"
                                                                )
                                                            ],
                                                            style={"text-align": "center"},
                                                            width=4
                                                        ),
                                                        dbc.Col(
                                                            [
                                                                dcc.Loading(
                                                                    [
                                                                        dcc.Graph(
                                                                            id="frequency-figure-1",
                                                                            config={'displayModeBar': False},
                                                                            style={"height": "27vh"}
                                                                        )
                                                                    ],
                                                                    type="circle",
                                                                    color="#ff7900"
                                                                )
                                                            ],
                                                            width=4,
                                                            className="h-100"
                                                        )
                                                    ],
                                                    className="d-flex justify-content-center align-items-center"
                                                ),
                                                dbc.CardFooter(
                                                    [
                                                        html.P("Mots enlevés")
                                                    ],
                                                    style={"display": "none"},
                                                    id="wc_footer"
                                                )
                                            ]
                                        )
                                    ],
                                    id="freq-body"
                                )
                            ],
                            style={'margin-top': '10px'}
                        )
                    ]
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        dbc.Button(
                                                            [
                                                                html.Span(className="fa fa-chevron-circle-down fa-2x")
                                                            ],
                                                            id="kw-header-expand-btn",
                                                            color="dark",
                                                            size="sm",
                                                            block=True,
                                                            className="h-100"
                                                        )
                                                    ],
                                                    width={'size': 1},
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Button(
                                                            [
                                                                html.H5(
                                                                    [
                                                                        "EXTRACTION AUTOMATIQUE - TF/Idf ".upper(),
                                                                        html.Span(className="fa fa-question-circle")
                                                                    ],
                                                                    style={
                                                                        "color": "#ff7900",
                                                                        "font-weight": "bolder",
                                                                        "margin-bottom": "0"
                                                                    }
                                                                )
                                                            ],
                                                            id="freq-modal-button",
                                                            className="border-0",
                                                            block=True
                                                        ),
                                                        dbc.Modal(
                                                            [
                                                                dbc.ModalHeader("Extraction automatique"),
                                                                dbc.ModalBody(p_7),
                                                                dbc.ModalFooter(
                                                                    dbc.Button("Close", id="freq-modal-close",
                                                                               className="ml-auto")
                                                                ),
                                                            ],
                                                            id="freq-modal",
                                                            centered=True,
                                                        )
                                                    ],
                                                    width={'size': 10},
                                                    style={'text-align': 'center'}
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Button(
                                                            [
                                                                html.Span(className="fa fa-chevron-circle-up fa-2x")
                                                            ],
                                                            id="kw-header-collapse-btn",
                                                            color="dark",
                                                            size="sm",
                                                            block=True,
                                                            className="h-100"
                                                        )
                                                    ],
                                                    width={'size': 1},
                                                )
                                            ]
                                        )
                                    ],
                                    style={"color": "#000", "background-color": "#fff"},
                                    className="border-0"
                                ),
                                dbc.Collapse(
                                    [
                                        dbc.CardBody(
                                            [
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            [
                                                                html.H5(
                                                                    id='supplier_selection_bis',
                                                                    style={
                                                                        'text-align': 'center',
                                                                        "color": "#ff7900",
                                                                        "background-color": "#000",
                                                                    },
                                                                    className="d-flex  h-100 w-100 align-items-center justify-content-center"
                                                                )
                                                            ],

                                                        ),
                                                        dbc.Col(
                                                            [
                                                                LEDDisplay(id='total_lo',
                                                                               label='Nb of Learning Objects',
                                                                               labelPosition='bottom',
                                                                               color='#ff7900',
                                                                               backgroundColor='#000')
                                                            ]
                                                        ),
                                                        dbc.Col(
                                                            [
                                                                LEDDisplay(id='active_lo',
                                                                               label='L.O. ACTIFS',
                                                                               labelPosition='bottom',
                                                                               color='#ff7900',
                                                                               backgroundColor='#000')
                                                            ]
                                                        ),
                                                        dbc.Col(
                                                            [
                                                                LEDDisplay(id='avg_score',
                                                                               label='% de Correspondance (moy.)',
                                                                               labelPosition='bottom',
                                                                               color='#ff7900',
                                                                               backgroundColor='#000')
                                                            ]
                                                        )
                                                    ]
                                                ),

                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            [
                                                                html.H5('Sélectionnez un Titre',
                                                                        style={
                                                                            'text-align': 'center'
                                                                        }),
                                                                html.Hr(className="border-top"),
                                                                dcc.Dropdown(id='title-dropdown')
                                                            ],
                                                            width={"size": 6, "offset": 3}
                                                        )
                                                    ]
                                                ),
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            [
                                                                html.H5("Description du Learning Object",
                                                                        style={'text-align': 'center'}),
                                                                html.Hr(className="border-top"),
                                                                html.P(id='description')
                                                            ],
                                                            id='col1',
                                                            width={"size": 6, "offset": 3}
                                                        )
                                                    ],
                                                    className="my-3"
                                                ),
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            [
                                                                html.H5('Mots \u00AB utiles \u00BB du Titre', style={'text-align': 'center'}),
                                                                # html.Hr(className="border-top"),
                                                                html.P(id='lemma-title', style={'text-align': 'center'})
                                                            ],
                                                            id='col2',
                                                            width={"size": 4, "offset": 2},
                                                            className="d-flex flex-column align-items-center justify-content-center"
                                                        ),
                                                        dbc.Col(
                                                            [
                                                                html.H5("Mots-clés (via TF-Idf) de la Description ", style={'text-align': 'center'}),
                                                                html.Hr(className="border-top"),
                                                                html.Div(id='tfidf-keywords', style={'width': '50%'}, className="d-flex align-items-center justify-content-center")
                                                            ],
                                                            id='col3',
                                                            width={"size": 4, "offset": 0},
                                                            className="d-flex flex-column align-items-center justify-content-center"

                                                        )
                                                    ],
                                                    className="my-3"
                                                ),

                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            [
                                                                html.H5('SCORE', style={'text-align': 'center'}),
                                                                html.P("Nombre de mots-clés extraits par tf-idf "
                                                                       "retrouvés dans le Titre",
                                                                       style={'text-align': 'center'}),
                                                                html.Hr(className="border-top"),
                                                                html.H2(id='lemma-score', style={'text-align': 'center'})
                                                            ],
                                                            id='col4',
                                                            width={"size": 4, "offset": 2}
                                                        ),
                                                        dbc.Col(
                                                            [
                                                                html.H5('% CORRESPONDANCE', style={'text-align': 'center'}),
                                                                html.P(' SCORE (colonne précédente) / Nombre de mots utiles du Titre)',
                                                                       style={'text-align': 'center'}),
                                                                html.Hr(className="border-top"),
                                                                html.H2(id='lemma-score-perc', style={'text-align': 'center'})
                                                            ],
                                                            id='col5',
                                                            width={"size": 4, "offset": 0}
                                                        )
                                                    ],
                                                    className="my-3"
                                                ),
                                                dbc.Row(
                                                    [
                                                        dbc.Button(
                                                            [
                                                                'AFFICHER TOUS LES L.O.'
                                                            ],
                                                            id='datatable_btn',
                                                            color='primary'
                                                        )
                                                    ]
                                                ),
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            [
                                                                dbc.Collapse(
                                                                    [
                                                                        DataTable(
                                                                            filter_action="native",
                                                                            id="kw-table",
                                                                            css=[{
                                                                                'selector': '.dash-spreadsheet td div',
                                                                                'rule': '''
                                                                                        line-height: 15px;
                                                                                        max-height: 150px; min-height: 150px; height: 150px;
                                                                                        display: block;
                                                                                        overflow-y: hidden;
                                                                                    '''
                                                                            }],
                                                                            style_cell_conditional=[
                                                                                {
                                                                                    "if": {"column_id": "lo_description"},
                                                                                    "textAlign": "right",
                                                                                    "whiteSpace": "normal",
                                                                                    "min-width": "45%",
                                                                                },
                                                                                {
                                                                                    "if": {"column_id": "tfidf_keywords_global"},
                                                                                    "textAlign": "right",
                                                                                    "whiteSpace": "normal",
                                                                                    "width": "14%",
                                                                                },
                                                                                {
                                                                                    "if": {"column_id": "lo_title"},
                                                                                    "textAlign": "left",
                                                                                    "whiteSpace": "normal",
                                                                                    "width": "25%"
                                                                                },
                                                                            ],
                                                                            style_data_conditional=[
                                                                                {
                                                                                    "if": {"row_index": "odd"},
                                                                                    "backgroundColor": "rgb(243, 246, 251)",
                                                                                }
                                                                            ],
                                                                            style_cell={
                                                                                "padding": "4px",
                                                                                "whiteSpace": "normal",
                                                                                "height": "auto",
                                                                                "max-width": 0,
                                                                            },
                                                                            style_header={"backgroundColor": "#ff7900",
                                                                                          "fontWeight": "bold"},
                                                                            style_data={"whiteSpace": "normal", "height": "auto"},
                                                                            page_size=5
                                                                        ),
                                                                        dbc.Button(['FERMER LA TABLE'], id='datatable_close_btn', color='primary')
                                                                    ],
                                                                    id='datatable_col',
                                                                ),
                                                            ]
                                                        )
                                                    ]
                                                ),
                                            ]
                                        )
                                    ],
                                    id="kw-body",
                                    is_open=False
                                )
                            ],
                            style={'margin-top': '10px'}
                        )
                    ]
                )
            ]
        )
    ],
    fluid=True
)
