import dash_bootstrap_components as dbc
import dash_html_components as html
from .textes import p_1, p_3, p_4, p_2, p_5
from .sidebar import encoded_image
import base64

content = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1(
                            "Le développement des compétences".upper(),
                            className="d-flex align-content-center",
                            style={"text-align": "right", "margin-top": "40px"}
                        ),
                        html.Img(
                            src='data:image/png;base64,{}'.format(encoded_image.decode()),
                            className="pl-3 pt-2",
                            height="75%",
                            style={"transform": "scaleXY(0.25,0.25)"}
                        )
                    ],
                    className="d-flex justify-content-center align-items-start",
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Div(
                                            [
                                                html.H3(
                                                    [
                                                        "146.768",
                                                        html.Sup(
                                                            [
                                                                html.I(className="fa fa-info-circle")
                                                            ],
                                                            id="nb-employees-tooltip",
                                                            style={"font-size": "1.6vmin"}
                                                        )
                                                    ],
                                                    className="d-flex align-items-center px-1"
                                                ),
                                                html.H6("employés en formation continue")
                                            ],
                                            id="",
                                            style={"font-weight": "900"},
                                            className="d-flex flex-column align-items-center justify-content-center"
                                        ),
                                        dbc.Tooltip(
                                            [
                                                "source: ",
                                                html.A(
                                                    [
                                                        "Rapport Financier 2019"
                                                    ],
                                                    id="",
                                                    href="https://www.orange.com/fr/content"
                                                         "/download/54121/1484030/version/2"
                                                         "/file/ORANGE_DEU_2019_VF.pdf"
                                                ),
                                            ],
                                            delay={"hide": 1000},
                                            target="nb-employees-tooltip",
                                            placement="top"
                                        )
                                    ],
                                    className="d-flex h-100 bordered justify-content-center text-center "
                                              "align-items-center",
                                    width={"size": 3, "offset": 0}
                                ),
                                dbc.Col(
                                    [
                                        html.H4([
                                            "1 OUTIL"
                                        ],
                                            style={"": ""},
                                            className=""
                                        ),
                                        html.H3(
                                            [
                                                "ORANGE  LEARNING"
                                            ],
                                            id="orange-learning-H5",
                                            style={"": ""},
                                            className=""
                                        ),
                                        dbc.Button(
                                            [html.Span(className="fa fa-question-circle fa-2x")],
                                            id="ol-modal-button",
                                            className="border-0",
                                            block=True,
                                            style={"font-size": "1vmin"}
                                        ),
                                        dbc.Modal(
                                            [
                                                dbc.ModalHeader("Orange Learning"),
                                                dbc.ModalBody([p_1]),
                                                dbc.ModalFooter(
                                                    dbc.Button("Close", id="ol-modal-close",
                                                               className="ml-auto")
                                                ),
                                            ],
                                            id="ol-modal",
                                            centered=True,
                                        )
                                    ],
                                    className="d-flex flex-column bordered justify-content-center text-center "
                                              "align-items-center",
                                    width={"size": 3, "offset": 0}
                                ),
                            ],
                            className="d-flex w-100 justify-content-center text-center align-items-center mb-3"
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.H5(
                                            [
                                                "« JOBS »"
                                            ],
                                            className="d-flex flex-column align-items-center "
                                                      "justify-content-center",
                                            style={"color": "#058ed9", "font-weight": "900"}
                                        ),
                                        html.Hr(className="border-top w-100"),
                                        p_2
                                    ],
                                    width={"size": 3, "offset": 0},
                                    className="d-flex flex-column justify-content-start align-items-center h-100 px-0",
                                ),
                                dbc.Col(
                                    [
                                        html.H5(
                                            [
                                                "« SKILLS »"
                                            ],
                                            className="d-flex flex-column justify-content-center align-items-center "
                                                      "justify-content-center",
                                            style={"color": "#47127f", "font-weight": "900"}
                                        ),
                                        html.Hr(className="border-top w-100"),
                                        p_3
                                    ],
                                    className="d-flex h-100 flex-column justify-content-start text-center "
                                              "align-items-center",
                                    width={"size": 3, "offset": 0}
                                ),
                                dbc.Col(
                                    [
                                        html.H5(
                                            [
                                                "« LEARNING OBJECTS »"
                                            ],
                                            id="lo-H5",
                                            style={"color": "#ff7900", "font-weight": "900"},
                                            className=""
                                        ),
                                        html.Hr(className="border-top w-100"),
                                        dbc.Button(
                                            [html.Span(className="fa fa-question-circle fa-3x")],
                                            id="lo-modal-button",
                                            className="border-0",
                                            block=True,
                                            style={"font-size": "1vmin", "background-color": "#ddd"}
                                        ),
                                        dbc.Modal(
                                            [
                                                dbc.ModalHeader("Learning Objects"),
                                                dbc.ModalBody([p_4, html.Br(), p_5]),
                                                dbc.ModalFooter(
                                                    dbc.Button("Fermer", id="lo-modal-close",
                                                               className="ml-auto")
                                                ),
                                            ],
                                            id="lo-modal",
                                            centered=True,
                                        )
                                    ],
                                    width={"size": 3, "offset": 0},
                                    className="d-flex h-100 flex-column justify-content-start text-center "
                                              "align-items-center",
                                ),
                            ],
                            className="d-flex justify-content-center text-center align-items-center w-100 my-1"
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        html.H4("OBJECTIF À MOYEN TERME")
                                                    ],
                                                    style={"color": "#ff7900", "font-weight": "900"},
                                                )
                                            ],
                                            className="h-50",
                                            style={"margin-top": "15px"}
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        html.H6(
                                                            [
                                                                "Intégrer une Intelligence Artificielle capable de "
                                                                "prédire quelle(s) ",
                                                                html.Span("SKILL", style={"color": "#47127f"}),
                                                                "(s) est (sont) développée(s) par quel(s) ",
                                                                html.Span("LEARNING OBJECT",
                                                                          style={"color": "#ff7900"}),
                                                                "(s) et par conséquent à quel(s) ",
                                                                html.Span("JOB", style={"color": "#058ed9"}),
                                                                "(s) ces derniers sont adressés."
                                                            ]
                                                        ),
                                                        html.Hr(className="border-top w-100"),
                                                    ],
                                                    className="d-flex h-100 flex-column justify-content-start "
                                                              "text-center align-items-center",
                                                    width={"size": 6, "offset": 3}
                                                )
                                            ],
                                            className="h-50",
                                            style={"margin-top": "15px"}
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        html.H4("3 OBJECTIFS À COURT TERME")
                                                    ],
                                                    style={"color": "#000000", "font-weight": "900"},
                                                )
                                            ],
                                            className="h-50",
                                            style={"margin-top": "5px"}
                                        ),
                                    ],
                                    className="d-flex flex-column justify-content-start align-items-center px-4 h-100",
                                ),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Row([dbc.Col([html.P("1: TABLEAU DE BORD", style={"font-weight": "750"})])], className="h-25"),
                                        dbc.Row([dbc.Col([html.P(
                                            "sur la répartition des quantités, types, statuts et catégories des "
                                            "Learning Objects + options \"vue globale\" ou \"vue personnalisée\" "
                                            "par \"Fournisseur de formations\"")])],
                                            className="h-50", style={"margin-top": "10px"})
                                    ],
                                    width={"size": 3, "offset": 0},
                                    className="d-flex flex-column justify-content-start align-items-center px-4 h-100",
                                ),
                                dbc.Col(
                                    [
                                        dbc.Row(
                                            [dbc.Col([html.P("2: EXTRACTION AUTOMATIQUE DE MOTS-CLÉS", style={"font-weight": "750"})])],
                                            className="h-25"),
                                        dbc.Row(
                                            [dbc.Col([html.P("""
                                            des Titres et des Descriptions correspondantes puis comparaison
                                            """),
                                                      html.P("""
                                            Les mots-clés de la Description d'un Learning Object se retrouvent-ils dans 
                                            son Titre ? (Optimisation du Moteur de Recherche)
                                            """)])],
                                            className="h-50", style={"margin-top": "10px"})
                                    ],
                                    width={"size": 3, "offset": 0},
                                    className="d-flex flex-column justify-content-start align-items-center px-4 h-100",
                                ),
                                dbc.Col(
                                    [
                                        dbc.Row(
                                            [dbc.Col([html.P("3: CLASSIFICATION DE DOCUMENTS", style={"font-weight": "750"})])],
                                            className="h-25"),
                                        dbc.Row(
                                            [dbc.Col([html.P("pour compléter automatiquement les Learning Objects dont "
                                                             "la catégorie est vide (Optimisation du Moteur de "
                                                             "Recherche)")])],
                                            className="h-50", style={"margin-top": "10px"})
                                    ],
                                    width={"size": 3, "offset": 0},
                                    className="d-flex flex-column justify-content-start align-items-center px-4 h-100",
                                ),
                            ],
                            className="d-flex justify-content-center text-center align-items-center w-100 my-4",
                            style={"margin-top": "25px"}
                        ),
                    ],
                    className="d-flex flex-column align-items-center"
                )
            ],
            className="d-flex flex-column align-items-center w-100"
        )
    ],
    fluid=True,
    className="d-flex flex-column mx-0",
    style={"max-width": "100%"}
)
