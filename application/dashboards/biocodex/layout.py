from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from .functions import mean_lat, mean_lon, datatable_cols, styles, legend1, legend2
from .functions import ugas_layer, pharmas_layer, target_layer, untarget_layer, info, ugas
import dash_leaflet as dl

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

table_content = dcc.Loading(
    [
        dcc.Store(id='memory'),
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Button(
                                    "FILTERS",
                                    id="open-offcanvas",
                                    n_clicks=0
                                ),
                                dbc.Label("PROFESSIONNELS DE SANTÉ", className="fw-bold"),
                                dash_table.DataTable(
                                    # data=id_adr.to_dict('records'),
                                    columns=datatable_cols,
                                    fixed_rows={'headers': True},
                                    page_size=20,
                                    filter_action="native",
                                    style_table={'overflowX': 'auto', 'fontSize': 12, 'font-family': '"Source Sans Pro", Helvetica, sans-serif', 'height': '600px'},
                                    style_data={"color": "black"},
                                    style_data_conditional=styles,
                                    style_header={'fontSize': 14, 'font_weight': 900, 'text-align': 'center', 'color': 'darkblue'},
                                    style_cell_conditional=[
                                        {'if': {'column_id': 'doc_id'}, 'textAlign': 'center'},
                                        {'if': {'column_id': 'nom'}, 'textAlign': 'left'},
                                        {'if': {'column_id': 'prenom'}, 'textAlign': 'left'},
                                        {'if': {'column_id': 'spe'}, 'textAlign': 'center'},
                                        {'if': {'column_id': 'pot'}, 'textAlign': 'center'},
                                        {'if': {'column_id': 'pvm'}, 'textAlign': 'center'},
                                        {'if': {'column_id': 'nv2022'}, 'textAlign': 'center'},
                                        {'if': {'column_id': 'etablissement'}, 'textAlign': 'center',  'textOverflow': 'ellipsis', 'fontSize': 12},
                                        {'if': {'column_id': 'uga'}, 'textAlign': 'center', 'fontSize': 12},
                                        {'if': {'column_id': 'adresse'}, 'textAlign': 'left', 'fontSize': 12},
                                        {'if': {'column_id': 'cp'}, 'textAlign': 'center', 'fontSize': 12},
                                        {'if': {'column_id': 'ville'}, 'textAlign': 'left', 'fontSize': 12},
                                        {'if': {'column_id': 'tel'}, 'textAlign': 'center', 'fontSize': 12}
                                    ],
                                    css=[
                                        {"selector": ".dash-spreadsheet-container tr th", "rule": "height: 16px;"},
                                        # set height of header
                                        {"selector": ".dash-spreadsheet-container tr", "rule": "height: 10px;"},
                                        # set height of body rows
                                        {"selector": ".dash-spreadsheet-inner", "rule": "max-height: calc('100vh - 226px')"}
                                    ],
                                    id="datatable"
                                )
                            ],
                            id="table-col"
                        )
                    ],
                    className="d-flex flex-row"
                ),
                dbc.Row(
                    [

                    ],
                    id="tile-content",
                ),
                offcanvas,
                dbc.Modal(
                    [
                        dbc.ModalHeader("END OF COMPLEX OPERATIONS"),
                        dbc.ModalBody("Finally!"),
                        dbc.ModalFooter(dbc.Button(id='close'))
                    ],
                    id='modal',
                    is_open=False,
                )
            ],
            style={"height": "100vh"},
            fluid=True,
            className="dbc"
        )
    ], type="circle"
)

map_content = html.Div(
    [
        # dcc.Checklist(id="uga-cl", value=["75AUT"], options=[{"value": uga, "label": uga} for uga in ugas], inline=True),
        dl.Map(
            [
               dl.LayersControl(
                    [
                        dl.BaseLayer(dl.TileLayer(), name="base", checked=True),
                        dl.Overlay(dl.LayerGroup(ugas_layer, id="ugas_layer_group"), name="ugas", checked=True),
                        dl.Overlay(dl.LayerGroup(pharmas_layer, id="pharmas_layer_group"), name="pharmas", checked=True),
                        dl.Overlay(dl.LayerGroup(target_layer, id="target_layer_group"), name="ciblés", checked=True),
                        dl.Overlay(dl.LayerGroup(untarget_layer, id="untarget_layer_group"), name="non ciblés", checked=False),
                        info
                    ]
               ),
                dl.FullScreenControl(),
                dl.LocateControl(locateOptions={'enableHighAccuracy': True})
           ],
           center=(mean_lat, mean_lon),
           zoom=11,
           style={'height': '90vh'}
        ),
        html.Div(id='tile-content')
    ],
    id='table-col'
)

button = html.Div(
    [
        dbc.Button(
            "Click me", id="example-button", className="me-2", n_clicks=0
        ),
        html.Span(id="example-output", style={"verticalAlign": "middle"}),
    ]
)


app_layout = html.Div(
    [
        dcc.Location(id='biocodex-url', refresh=False),
        html.Div(id="page-content", className="container-fluid", style={"max-width": "94vw"})
    ],
    id="dash-wrapper"
)


def build_layout():
    return app_layout
