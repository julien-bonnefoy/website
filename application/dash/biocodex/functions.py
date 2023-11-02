from sqlalchemy import create_engine, func, extract
from sqlalchemy.orm import Session
from application.pds.models import db, Cdb, Connections, Identity, Adress
import pandas as pd
from dash import html, dash_table, dcc
import dash_bootstrap_components as dbc
from stem import Signal
import numpy as np
import os
from application.config import basedir
from dotenv import load_dotenv
import re
import requests
from datetime import datetime
from stem.control import Controller

load_dotenv(os.path.join(basedir, '.env'))
DATABASE_URL = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://')
engine = create_engine(DATABASE_URL)

ugas = ["75AUT", "75PAS", "75TRO", "75ELY", "75INV", "75GRE", "75VAU", "75MNP", "75PER", "75TER", "92LEV", "92NEU"]
spes = ["GY", "MG-GY", "SF", "MG", "GE", "PE", "PE-PSY", "PSY", "NE"]
cibles = ["HC", 1, 2, 3, 4]
doctor_colors = {
    'GY': '#bd0071',
    'MG-GY': '#bd0071',
    'SF': '#bd0071',
    'MG': '#aaa',
    'GE': '#fe7600',
    'PE': '#007fff',
    'PE-PSY': '#410E66',
    'PSY': '#410E66',
    'NE': '#410e66',
}
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


def join_id_adr():

    with Session(engine) as session:
        id_adr = pd.read_sql_query(
            sql=session.query(
                Connections.doc_id, Identity.nom, Identity.prenom, Identity.spe, Identity.pot, Identity.pvm,
                Identity.nv22, Identity.cib, Identity.dec, Adress.eta, Adress.uga, Adress.adr, Adress.cp, Adress.ville, Adress.tel,
                Adress.lat, Adress.lon
            ).join(Identity).join(Adress).statement,
            con=engine
        )
        session.close()

    return id_adr


def join_id_cdb():

    with Session(engine) as session:
        id_cdb = pd.read_sql_query(
            sql=session.query(
                Connections.doc_id, Identity.nom, Identity.prenom, Identity.spe, Identity.pot, Identity.pvm,
                Identity.nv22, Identity.cib, Identity.dec,
                Cdb.mode, Cdb.com, Cdb.ddv, Cdb.dpv, Cdb.rdv, Cdb.rec, Cdb.pk, Cdb.lun_mat, Cdb.lun_am, Cdb.mar_mat, Cdb.mar_am, Cdb.mer_mat, Cdb.mer_am, Cdb.jeu_mat, Cdb.jeu_am,
                Cdb.ven_mat, Cdb.ven_am,
            ).join(Identity).join(Cdb).statement,
            con=engine
        )
        session.close()

    return id_cdb


def join_id_adr_cdb():

    with Session(engine) as session:
        id_adr_cdb = pd.read_sql_query(
            sql=session.query(
                Connections.doc_id, Identity.nom, Identity.prenom, Identity.spe, Identity.pot, Identity.pvm,
                Identity.nv22, Identity.cib, Identity.dec,
                Adress.eta, Adress.uga, Adress.adr, Adress.cp, Adress.ville, Adress.tel, Adress.lat, Adress.lon,
                Cdb.mode, Cdb.com, extract("EPOCH", Cdb.ddv), extract("EPOCH", Cdb.dpv), Cdb.rdv, Cdb.rec, Cdb.pk,
                Cdb.lun_mat, Cdb.lun_am, Cdb.mar_mat, Cdb.mar_am, Cdb.mer_mat, Cdb.mer_am, Cdb.jeu_mat, Cdb.jeu_am,
                Cdb.ven_mat, Cdb.ven_am
            ).join(Identity).join(Adress).join(Cdb).statement,
            con=engine
        )
        session.close()
        id_adr_cdb.columns = [
            'id', 'nom', 'prenom', 'spe', 'pot', 'pvm', 
            'nv22', 'cib', 'dec',
            'eta', 'uga', 'adr', 'cp', 'ville', 'tel', 'lat', 'lon', 
            'mode', 'com', 'ddv', 'dpv', 'rdv', 'rec', 'pk',
            'lun_mat', 'lun_am', 'mar_mat', 'mar_am', 'mer_mat', 'mer_am', 'jeu_mat', 'jeu_am',
            'ven_mat', 'ven_am'
        ]
    return id_adr_cdb


def discrete_background_color_bins(df, n_bins=5, columns=['all'], colorscale="Blues"):
    import colorlover
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    if columns == ['all']:
        if 'id' in df:
            df_numeric_columns = df.select_dtypes('int64').drop(['id'], axis=1)
        else:
            df_numeric_columns = df.select_dtypes('int64')
    else:
        df_numeric_columns = df[columns]
    df_max = df_numeric_columns.max().max()
    df_min = df_numeric_columns.min().min()
    ranges = [
        ((df_max - df_min) * i) + df_min
        for i in bounds
    ]
    styles = []
    legend = []
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        backgroundColor = colorlover.scales[str(n_bins)]['seq'][colorscale][i - 1]
        color = 'white' if i > len(bounds) / 2. else 'inherit'

        for column in df_numeric_columns:
            styles.append({
                'if': {
                    'filter_query': (
                        '{{{column}}} >= {min_bound}' +
                        (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                    ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                    'column_id': column
                },
                'backgroundColor': backgroundColor,
                'color': color
            })
        legend.append(
            html.Div(style={'display': 'inline-block', 'width': '30px'}, children=[
                html.Div(
                    style={
                        'backgroundColor': backgroundColor,
                        'borderLeft': '1px rgb(50, 50, 50) solid',
                        'height': '10px'
                    }
                ),
                html.Small(int(min_bound), style={
                    'paddingLeft': '2px',
                    'color': 'black',
                    'textOrientation': 'upright',
                    'fontSize': 8}
                           )
            ])
        )

    return (styles, html.Div(legend, style={'padding': '5px 0 5px 0', 'color': 'white'}))


def get_compo(df):
    idx = pd.IndexSlice
    compo = df.pivot_table(values="nom", index=["uga", "spe"], columns="cib", aggfunc='count').fillna(0).astype(int)
    compo = compo[[2, 3, 4, 0]]
    compo.columns = ["2x", "3x", "4x", "non ciblé"]
    compo.index.name = None
    new_index = pd.MultiIndex.from_product([
        ugas,
        spes
    ], names=["uga", "spe"])
    compo.reindex(new_index)

    return compo


def get_uga_compo(compo, uga):
    compo = compo.loc[[uga, ], :].reset_index().drop("uga", axis=1)
    for col in ["2x", "3x", "4x"]:
        compo[col] = np.where(compo[col] == 0, '', compo[col])

    return compo


def get_info(df, feature=None):
    header = [html.H4("Composition")]
    if not feature:
        return header + [html.P("Hoover over a UGA")]
    uga_compo = get_uga_compo(get_compo(df), feature["properties"]["CODE_UGA"])
    table = dash_table.DataTable(
        uga_compo.to_dict('records'),
        [{"name": i.upper(), "id": i} for i in uga_compo.columns],
        style_cell_conditional=[
            {
                'if': {'column_id': 'spe'},
                'textAlign': 'left'
            }
        ],
        style_header={'width': '50px', 'border': '1px solid black', 'textAlign': 'center'},
        style_cell={'width': '50px', 'border': '1px solid grey', 'textAlign': 'center'},
    )
    return header + [html.B(feature["properties"]["CODE_UGA"]), table]


def unix_to_dt(unix):
    from datetime import datetime
    if type(unix) == str:
        ts = int(unix)
    else:
        ts = unix
    return datetime.utcfromtimestamp(ts).strftime('%d/%m/%Y %H:%M')


def prepare_data(df):

    df['nv22'] = np.where(df['nv22'] == 0, '', df["nv22"])
    df['nv22'] = [int(nv) if nv != '' else '' for nv in df['nv22']]

    df['cib'] = np.where(df['cib'] == 0, 'HC', df["cib"])
    df['cib'] = [int(c) if c != 'HC' else 'HC' for c in df['cib']]

    df['rdv'] = ['\u2705' if pd.isnull(row['dpv']) == 0 else '' for i, row in df.iterrows()]

    df.sort_values(['uga', 'adr', 'spe', 'pot', 'pvm'], ascending=[True, True, True, False, False], inplace=True)

    return df


def formalize(row):
    cdb = db.session.get(Cdb, row['cdb_id'])
    return [
        dbc.Form(
            [
                dbc.Row([
                    dbc.FormFloating(
                        [
                            dbc.Input(value=row['cdb_id'], name='cdb_id'), dbc.Label('cdb_id', className="pl-2")
                        ],
                        className="col-2"
                    ),
                    dbc.FormFloating(
                        [
                            dbc.Input(value=row['adr_id'], disabled=True, name='adr_id'),
                            dbc.Label('adr_id', className='pl-2')
                        ],
                        className="col-2"
                    ),
                    dbc.FormFloating(
                        [
                            dbc.Input(value=row['doc_id'], disabled=True, name='doc_id'),
                            dbc.Label('doc_id', className='pl-2')
                        ],
                        className="col-2"
                    ),
                ], className="px-4 mb-4", justify='between'),
                dbc.Row([
                    dbc.FormFloating(
                        [
                            dbc.Input(value=cdb.com, type="hidden", name='old'),
                            dbc.Input(value=cdb.com, type="text", name='new'), dbc.Label('com', className="pl-2")
                        ],
                        className="col-6"
                    )
                ], className="px-4 mb-4", justify='between'),
            ],
            id="form-modal"
        )

    ]


def generate_html_table_from_df(df):
    Thead = html.Thead(
        [html.Tr([html.Th(col) for col in df.columns])]
    )
    Tbody = html.Tbody(
        [html.Tr(
            [html.Td( df.iloc[i, j], id = '{}_{}_{}'.format(id, i, j) ) for j in range(len(df.columns))]
         ) for i in range(len(df))]
    )
    return [Thead, Tbody]


def build_tile_front(row):
    connection = Connections.query.filter(Connections.doc_id == row['id']).first()
    now = datetime.now()
    ddv = None
    dpv = None

    if row["mode"] == "RAPPELER":
        color = 'warning'
    elif row["mode"] == "CHECK":
        color = 'info'
    elif row["mode"] == "L":
        color = 'info'
    else:
        color = "secondary"

    if type(row['dpv']) == int :
        dpv = unix_to_dt(row['dpv'])
        if row['dpv'] < now.timestamp():
            color = 'danger'
        elif row['dpv'] > now.timestamp():
            color = 'success'

    badge_color = "secondary"
    if type(row['ddv']) == int:
        ddv = unix_to_dt(row['ddv'])
        if row['ddv'] >= int(pd.to_datetime("01/08/2023 00:00", dayfirst=True).timestamp()):
            badge_color = 'success'

    return dbc.Card(
        [
            dbc.CardHeader(
                [
                    html.Button(
                        [
                            html.Pre(f'{row["nom"]} {row["prenom"].title()}', className="mb-0",
                                     style={"fontSize": "14px", "textDecoration": "none"})
                        ],
                        id="modal-btn",
                        className=f"btn btn-{color} d-block fw-bold w-100",
                        **{"data-ref" : f"/dash/biocodex/pds/{row['id']}"}
                    ),
                    dbc.Badge(row['uga'], color="light", text_color="black", className="my-1 w-25",
                              style={"fontSize": "8px", "align-self": "center"}
                    ),
                    html.Div([
                        dbc.FormFloating([
                            dbc.Input(value=row['pot'], id="pot-input", size="sm",
                                      style={"fontSize": "9px", "maxHeight": "30px", "minHeight": "30px",
                                             "height": "30px", "textAlign": "right"}, className="pt-3"),
                            dbc.Label('pot', size="sm", style={"fontSize": "8px"}, className="px-1 py-2")
                        ], style={"maxHeight": "30px", "minHeight": "30px", "height": "30px"}, className="col-3"),
                        dbc.FormFloating([
                            dbc.Input(value=row['pvm'], id=f"pvm-input", size="sm",
                                      style={"fontSize": "9px", "maxHeight": "30px", "minHeight": "30px",
                                             "height": "30px", "textAlign": "right"}, className="pt-3"),
                            dbc.Label('PVM', size="sm", style={"fontSize": "8px"}, className="px-1 py-2")
                        ], style={"maxHeight": "30px", "minHeight": "30px", "height": "30px"}, className="col-3"),
                        dbc.FormFloating([
                            dbc.Input(value=row['nv22'], id=f"nv22-input", size="sm",
                                      style={"fontSize": "9px", "maxHeight": "30px", "minHeight": "30px",
                                             "height": "30px", "textAlign": "right"}, className="pt-3"),
                            dbc.Label('nv 22', size="sm", style={"fontSize": "8px"}, className="px-1 py-2")
                        ], style={"maxHeight": "30px", "minHeight": "30px", "height": "30px"}, className="col-3"),
                        dbc.FormFloating([
                            dbc.Input(value=row['dec'], id="dec-input", size="sm",
                                      style={"fontSize": "9px", "maxHeight": "30px", "minHeight": "30px",
                                             "height": "30px", "textAlign": "right"}, className="pt-3"),
                            dbc.Label('décile', size="sm", style={"fontSize": "8px"}, className="px-1 py-2")
                        ], style={"maxHeight": "30px", "minHeight": "30px", "height": "30px"}, className="col-3")
                    ], className="d-flex")
                ],
                className="d-flex flex-column flex-wrap"
            ),
            dbc.CardBody(
                [
                    html.Div([
                        dbc.FormFloating([
                            dbc.Input(value=row['com'], id="com-input", size="sm",
                                      style={"fontSize": "12px", "maxHeight": "40px", "minHeight": "40px",
                                             "height": "40px", "textAlign": "right"}, className="pt-3"),
                            dbc.Label('com', size="sm", style={"fontSize": "10px"})
                        ], style={"maxHeight": "40px", "minHeight": "40px", "height": "40px"}, className="w-100"),
                        dbc.FormFloating([
                            dbc.Input(value=row['mode'], id="mode-input", size="sm",
                                      style={"fontSize": "12px", "maxHeight": "40px", "minHeight": "40px",
                                             "height": "40px", "textAlign": "right"}, className="pt-3"),
                            dbc.Label('mode', size="sm", style={"fontSize": "10px", "backgroundColor": "white"})
                        ], style={"maxHeight": "40px", "minHeight": "40px", "height": "40px"}, className="d-flex"),
                    ], className="d-block")
                ]
            ),
            dbc.CardFooter(
                [
                    html.Div([
                        dbc.FormFloating([
                            dbc.Input(value=row['rec'], id="rec-input", size="sm",
                                      style={"fontSize": "9px", "maxHeight": "30px", "minHeight": "30px",
                                             "height": "30px", "textAlign": "right"}, className="pt-3"),
                            dbc.Label('recoit ?', size="sm", style={"fontSize": "8px"}, className="px-1 py-2")
                        ], style={"maxHeight": "30px", "minHeight": "30px", "height": "30px"},
                            className="ms-auto w-50"),
                        dbc.FormFloating([
                            dbc.Input(value=row['pk'], id=f"pk-input", size="sm",
                                      style={"fontSize": "9px", "maxHeight": "30px", "minHeight": "30px",
                                             "height": "30px", "textAlign": "right"}, className="pt-3"),
                            dbc.Label('if not, why?', size="sm", style={"fontSize": "8px"}, className="px-1 py-2")
                        ], style={"maxHeight": "30px", "minHeight": "30px", "height": "30px"}, className="w-50")
                    ], className="d-flex"),
                    html.Div([
                        dbc.FormFloating([
                            dbc.Input(value=ddv, id="ddv-input", size="sm",
                                      style={"fontSize": "9px", "maxHeight": "40px", "minHeight": "40px",
                                             "height": "40px", "textAlign": "right"}, className="pt-4"),
                            dbc.Label('ddv', size="sm", style={"fontSize": "10px"})
                        ], style={"maxHeight": "40px", "minHeight": "40px", "height": "40px"},  className="ms-auto w-50"),
                        dbc.FormFloating([
                            dbc.Input(value=dpv, id=f"dpv-input", size="sm",
                                      style={"fontSize": "9px", "maxHeight": "40px", "minHeight": "40px",
                                             "height": "40px", "textAlign": "right"}, className="pt-4"),
                            dbc.Label('dpv', size="sm", style={"fontSize": "10px"})
                        ], style={"maxHeight": "40px", "minHeight": "40px", "height": "40px"}, className="w-50")
                    ], className="d-flex")
                ]
            ),
            html.Span(
                html.Img(
                    [],
                    src="assets/img/blue_turn.png",
                    height=32,
                    width=32,
                    style={"transform": "translate(75%, 50%)", "zIndex": "1"},
                    className="arrow position-absolute bottom-0 end-100"
                )
            ),
            html.Div(
                [
                    row["spe"]
                ],
                id="spe-badge-front",
                className="badge position-absolute top-0 start-0 translate-middle",
                style={
                    "color": "#FFFFFF",
                    "fontWeight": 900,
                    "fontSize": "11px",
                    "backgroundColor": f"{doctor_colors[row['spe']]}",
                    "transform": "rotateZ(45deg)"
                },
                **{"data-tor": "place.left place.top"}
            ),
            dbc.Badge([f"{row['cib']}", html.Span([], className="visually-hidden")],
                  id="cib-badge-front",
                  className=f"position-absolute bottom-0 start-100 bg-{badge_color}",
                  style={"fontSize": "12px", "transform": "translate(-50%, 50%)"}
            )
        ],
        className="flip-card-front",
        style={"backgroundColor": "#FFFFFF", "opacity": "1"}
    )


def build_tile_back(row):
    connection = Connections.query.filter(Connections.doc_id == row['id']).first()
    return dbc.Card(
        [
            dbc.CardHeader(
                [
                    dbc.Button(
                        [
                            html.Pre(f'{row["nom"]} {row["prenom"].title()}', className="mb-0",
                                     style={"fontSize": "14px"})
                        ],
                        className="d-block w-100",
                        href=check_doctolib_profile(connection.id),
                        outline=True,
                        color='light'
                    ),
                    dbc.Col(
                        [
                            dbc.Badge(row['tel'], color="primary", text_color="white", className="border w-75",
                                      style={"fontSize": "14px"}),
                            dbc.Badge(row['uga'], color="primary", text_color="white", className="border my-1 w-25",
                                      style={"fontSize": "10px", "align-self": "center"}),
                        ],
                        className="d-flex flex-row align-items-start justify-content-between my-1",
                    )
                ],
                className="d-flex flex-column"
            ),
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.FormFloating([
                                dbc.Input(value=row['adr'], id="adr-input", size="sm",
                                          style={"fontSize": "12px", "maxHeight": "40px", "minHeight": "40px",
                                                 "height": "40px", "textAlign": "right"}, className="pt-3"),
                                dbc.Label('adr', size="sm", style={"fontSize": "10px"})
                            ], style={"maxHeight": "30px", "minHeight": "30px", "height": "30px"},
                                className="w-100")
                        ]),
                    dbc.Row(
                        [
                                dbc.FormFloating([
                                    dbc.Input(value=row['cp'], id="cp-input", size="sm",
                                              style={"fontSize": "12px", "maxHeight": "40px", "minHeight": "40px",
                                                     "height": "40px", "textAlign": "right"}, className="pt-3"),
                                    dbc.Label('cp', size="sm", style={"fontSize": "10px"})
                                ], style={"maxHeight": "30px", "minHeight": "30px", "height": "30px"}, className="w-50"
                                ),
                                dbc.FormFloating([
                                    dbc.Input(value=row['ville'], id="ville-input", size="sm",
                                              style={"fontSize": "12px", "maxHeight": "40px", "minHeight": "40px",
                                                     "height": "40px", "textAlign": "right"}, className="pt-3"),
                                    dbc.Label('ville', size="sm", style={"fontSize": "10px"})
                                ], style={"maxHeight": "30px", "minHeight": "30px", "height": "30px"}, className="w-50"
                                )
                        ])
                ], style={"opacity": 1}),
            dbc.CardFooter(
                [
                    dbc.Button("SAVE & CLOSE", id="save-btn-tile", className="ml-auto btn btn-sm")
                ]
            ),
            html.Div(
                [
                    row["spe"]
                ],
                id="spe-badge-back",
                className="badge position-absolute top-0 start-100 translate-middle",
                style={
                    "color": "#FFFFFF",
                    "fontWeight": 900,
                    "fontSize": "11px",
                    "backgroundColor": f"{doctor_colors[row['spe']]}",
                },
                **{"data-tor": "place.left place.top"}
            ),
            html.Span(
                [
                    f"{row['cib']}",
                    html.Span([], className="visually-hidden")
                ],
                id="cib-badge-back",
                className="position-absolute bottom-0 start-0 badge bg-dark",
                style={"fontSize": "12px", "transform": "translate(-50%, 50%)"}
            ),
            html.Span(
                html.Img([],
                 src="assets/img/blue_turn.png",
                 height=32,
                 width=32,
                 style={"transform": "translate(-75%, 50%) rotateY(180deg)", "zIndex": "1"},
                 className="arrow position-absolute bottom-0 start-100"
                 ),
            )
        ],
        className="flip-card-back border border-secondary border-2 h-100"
    )


def build_flip(row):

    return dbc.Col(
        [
            html.Div(
        [
                    html.Div(
                        [
                            build_tile_front(row),
                            build_tile_back(row)
                        ],
                        className="flip-card-inner"
                    )
                ],
                className="flip-card m-4"
            ),
            dbc.Modal(
                [
                    dbc.ModalHeader(id="modal-header"),
                    dbc.ModalBody(id="modal-body"),
                    dbc.ModalFooter(
                        [
                            dbc.Button("CLOSE", id="close-btn-modal", className="btn btn-sm ml-auto"),
                            dbc.Button("SAVE & CLOSE", id="save-btn-modal", className="btn btn-sm ml-auto")
                        ],
                        id="modal-footer"
                    ),
                ],
                id="pds-modal",
                is_open=False
            )
        ],
        className="col-xl-2 col-sm-6"
    )


def build_modal_flip(row):
    return dbc.Col(
        [
            html.Div(
        [
                    html.Div(
                        [
                            build_tile_front(row),
                            build_tile_back(row)
                        ],
                        className="flip-card-inner"
                    )
                ],
                className="flip-card m-4"
            )
        ]
    )


def switchIp():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate("welcome")
        controller.signal(Signal.NEWNYM)


def get_tor_session():
    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {
        'http':  'socks5://127.0.0.1:9050',
        'https': 'socks5://127.0.0.1:9050'
    }
    session.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)'}
    return session


def check_doctolib_profile(conn_id):
    switchIp()
    connection = Connections.query.filter(Connections.id==conn_id).first()
    doctor = connection.doc
    prenom = doctor.prenom.lower().replace(' ', '-')
    nom = doctor.nom.lower().replace(' ', '-')
    spe=doctors_spes[doctor.spe]
    adress=connection.adr
    ville = adress.ville.lower()
    return f"https://www.doctolib.fr/{spe}/{ville}/{prenom}-{nom}"


id_adr = join_id_adr()
(styles1, legend1) = discrete_background_color_bins(id_adr, n_bins=9, columns=["pvm"])
(styles2, legend2) = discrete_background_color_bins(id_adr, n_bins=9, columns=["pot"], colorscale="YlGn")
styles = styles1 + styles2

df = join_id_adr_cdb()
mean_lat = df['lat'].mean()
mean_lon = df['lon'].mean()

data_df = prepare_data(df)
datatable_cols =[{"name": i.upper(), "id": i} for i in data_df.columns]


