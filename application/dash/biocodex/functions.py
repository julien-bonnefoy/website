from sqlalchemy import create_engine, func, extract
from sqlalchemy.orm import Session
from application.dash.biocodex.models import Cdb, Connections, Identity, Adress
import pandas as pd
from dash import html, dash_table
import dash_bootstrap_components as dbc
#from stem import Signal
import numpy as np
import os
from application.config import basedir
from dotenv import load_dotenv
import requests
from datetime import datetime
# from stem.control import Controller
import dash_leaflet as dl
import dash_leaflet.express as dlx
import json
import io
from flask import render_template


load_dotenv(os.path.join(basedir, '.env'))
DATABASE_URL = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://')
engine = create_engine(DATABASE_URL)

ugas = ["75AUT", "75PAS", "75TRO", "75ELY", "75INV", "75GRE", "75VAU", "75MNP", "75PER", "75TER", "92LEV", "92NEU"]
spes = ["GY", "MGY", "SF", "MG", "GE", "PE", "PPSY", "PSY", "NE"]
cibles = ["HC", 1, 2, 3, 4]
doctor_colors = {
    'GY': '#bd0071',
    'MGY': '#bd0071',
    'SF': '#bd0071',
    'MG': '#aaa',
    'GE': '#fe7600',
    'PE': '#0080ff',
    'PPSY': '#410E66',
    'PSY': '#410E66',
    'NE': '#410e66',
    '': '#000000'
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


def prepare_data(df):

    df['nv22'] = np.where(df['nv22'] == 0, '', df["nv22"])
    df['nv22'] = [int(nv) if nv != '' else '' for nv in df['nv22']]

    df['cib'] = np.where(df['cib'] == 0, 'HC', df["cib"])
    df['cib'] = [int(c) if c != 'HC' else 'HC' for c in df['cib']]

    df['rdv'] = ['\u2705' if pd.isnull(row['dpv']) == 0 else '' for i, row in df.iterrows()]

    df.sort_values(['uga', 'adr', 'spe', 'pot', 'pvm'], ascending=[True, True, True, False, False], inplace=True)

    return df


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

        df=prepare_data(id_adr_cdb)

    return df



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
                        'height': '11px'
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


def build_tile_front(row, in_modal=False, need_form = False):
    if row['tel'] == "":
        row['tel'] = "  .  .  .  .  "


    now = datetime.now()
    ddv = None
    dpv = None

    if row["mode"] == "RAPPELER" or row["com"] == "RAPPELER":
        color = 'warning'
    elif row["mode"] == "CHECK":
        color = 'info'
    elif row["mode"] == "L":
        color = 'info'
    else:
        color = "secondary"

    if not pd.isnull(row['dpv']):
        if type(row['dpv']) == int or type(row['dpv']) == float :
            dpv = unix_to_dt(row['dpv'])
            if row['dpv'] < now.timestamp():
                color = 'danger'
            elif row['dpv'] > now.timestamp():
                color = 'success'

    badge_color = "secondary"
    if not pd.isnull(row['ddv']):
        if type(row['ddv']) == int or type(row['ddv']) == float:
            ddv = unix_to_dt(row['ddv'])
            if row['ddv'] >= int(pd.to_datetime("01/08/2023 00:00", dayfirst=True).timestamp()):
                badge_color = 'success'
                color="success"

    btn_id = {"type": "modal-open", "index": row['id']}
    sub_id = {"type": "submit", "index": row['id']}
    form_id = f"form-{row['id']}"
    arrow_class = "d-block"
    shield_class = "d-block p-0 border-0"
    save_btn_style = {"display": "none"}
    disabled=True
    hide = "hide"
    front_style = {"backgroundColor": "#FFFFFF", "opacity": 1}
    if in_modal:
        btn_id = f"btn-{row['id']}"
        sub_id = f"sub-{row['id']}"
        form_id = {"type": "form", "index": row['id']}
        arrow_class = shield_class = "d-none"
        save_btn_style = {"display": "block"}
        disabled=False
        hide=""
        front_style = {"backgroundColor": "#FFFFFF", "opacity": 0.5, "width": "330px"}


    cbody = dbc.CardBody(
        [
            html.Div(
                [
                    dbc.FormFloating([
                        dbc.Input(disabled=disabled, value=row['adr'], name="adr", size="sm", className="pt-3"),
                        dbc.Label('ADRESSE', size="sm", className="px-1 py-2 bg-transparent"),
                    ], className="border-3 border-info col-12 px-0")
                ], className="d-flex"),
                html.Div([
                    dbc.Badge(dbc.Input(disabled=disabled, value=row['tel'], name="tel", size="sm", className="text-bold my-2 col-5", style={"font-size": "10px"}),
                              color="#FFFFFF", style={"opacity": .5, "color": "#000080"}),
                    dbc.FormFloating([
                        dbc.Input(disabled=disabled, value=row['cp'], name="cp", size="sm", className="pt-3"),
                        dbc.Label('CP', size="sm", className="px-1 py-2 bg-transparent")
                    ], className="border-3 border-info col-3 px-0"),
                    dbc.FormFloating([
                        dbc.Input(disabled=disabled, value=row['ville'], name="ville", size="sm", className="pt-3",
                                  style={"font-size": "11px", "overflow-x": "hidden"}),
                        dbc.Label('VILLE', size="sm", className="px-1 py-2 bg-transparent")
                    ], className="border-3 border-info col-4 px-0"),
                ], className="d-flex"),
                html.Br(),
                html.Div([
                    dbc.FormFloating([
                        dbc.Input(disabled=disabled, value=row['rec'], name="rec", size="sm",
                                  className="pt-3"),
                        dbc.Label('REÇOIT ?', size="sm", className="px-1 py-2 bg-transparent")
                    ], className="border-3 border-info col-4 px-0"),
                    dbc.FormFloating([
                        dbc.Input(disabled=disabled, value=row['mode'], name="mode", size="sm",
                                  className="pt-3"),
                        dbc.Label('MODE', size="sm", className="px-1 py-2 bg-transparent")
                    ], className="border-3 border-info col-4 px-0"),
                    dbc.FormFloating([
                        dbc.Input(disabled=disabled, value=row['pk'], name="pk", size="sm",
                                  className="pt-3"),
                        dbc.Label('IF NOT, WHY?', size="sm", className="px-1 py-2 bg-transparent")
                    ], className="border-3 border-info col-4 px-0")
                ], className="d-flex"),
                html.Div([
                    dbc.FormFloating([
                        dbc.Input(disabled=disabled, value=row['com'], name="com", size="sm",
                                  className="pt-3"),
                        dbc.Label('COMMENT.', size="sm", className="px-1 py-2 bg-transparent")
                    ], className="border-3 border-info col-12 px-0")
                ], className="d-flex" )
        ],
        id={"type": "card-body", "index": row['id']},
        style={"flex": "0 1 auto"},
        className=hide
    )

    cfooter = dbc.CardFooter(
        [
            html.Div(
                [
                    dbc.FormFloating([
                        dbc.Input(disabled=disabled, value=ddv, name="ddv", size="sm", className="pt-4"),
                        dbc.Label('DDV', size="sm", className="px-1 py-2 bg-transparent")
                    ], className="ms-auto w-50"),
                    dbc.FormFloating([
                        dbc.Input(disabled=disabled, value=dpv, name="dpv", size="sm", className="pt-4"),
                        dbc.Label('DPV', size="sm", className="px-1 py-2 bg-transparent")
                    ], className="w-50")
                ],
                className="d-flex"
            )
        ],
        className="p-3"
    )

    input = dbc.Input(
        id=sub_id,
        value="SAVE & CLOSE",
        className="btn btn-xl mx-auto",
        type="submit",
        style=save_btn_style
    )

    form = html.Form(
        [
            cbody,
            cfooter,
            input
        ],
        id = form_id,
        method = 'post',
        action = f'/dash/biocodex/pds/{row["id"]}'
    )

    card_content = html.Div([cbody, cfooter, input])

    if need_form:
        card_content = form

    potentiel = dbc.FormFloating(
        [
            dbc.Input(disabled=True, value=row['pot'], name="pot", size="sm", className="pt-3 fw-bolder bg-light"),
            dbc.Label('POTENTIEL', size="sm", className="px-1 py-2 bg-transparent")
        ],
        className="border-3 border-info col-3"
    )

    pvm = dbc.FormFloating(
        [
            dbc.Input(disabled=True, value=row['pvm'], id=f"pvm-input", size="sm", className="pt-3 fw-bolder bg-light"),
            dbc.Label('PVM', size="sm", className="px-1 py-2 bg-transparent")
        ],
        className="border-3 border-info col-3")

    nv22 = dbc.FormFloating(
        [
            dbc.Input(disabled=True, value=row['nv22'], id=f"nv22-input", size="sm", className="pt-3 fw-bolder bg-light"),
            dbc.Label('NV 2022', size="sm", className="px-1 py-2 bg-transparent")
        ],
        className="border-3 border-info col-3"
    )

    decile = dbc.FormFloating(
        [
            dbc.Input(disabled=True, value=row['dec'], name="dec", size="sm", className="pt-3 fw-bolder bg-light"),
            dbc.Label('DÉCILE', size="sm", className="px-1 py-2 bg-transparent")
        ],
        className="border-3 border-info col-3"
    )

    kpis = []
    if row["spe"] == "PSY" or row["spe"] == "PPSY":
        kpis=[potentiel, pvm, nv22, decile]
    else:
        kpis = [potentiel, pvm, nv22]

    return dbc.Card(
        [
            dbc.Badge(
                row['uga'],
                id={"type": "uga-badge-front", "index": row["id"]},
                className="uga-badge position-absolute top-0 start-100  bg-white"
            ),
            dbc.Badge(
                row['spe'],
                id={"type": "spe-badge-front", "index": row["id"]},
                color=f"{doctor_colors[row['spe']]}",
                text_color="white",
                className="spe-badge my-1 position-absolute top-0 start-0"
            ),
            dbc.Badge(
                [row['cib'], html.Span([], className="visually-hidden")],
                id="cib-badge-front",
                className=f"position-absolute top-100 start-100 bg-{badge_color}",
                style={"fontSize": "13px", "transform": "translate(-50%, -50%)"}
            ),
            html.Span(
                html.Img(
                    [],
                    id={"type": "blue-arrow-btn-front", "index": row['id']},
                    src="assets/img/blue_turn.png",
                    height=25,
                    width=25,
                    style={"position": "absolute", "zIndex": "1", "transform": "translate(-25%, -50%)"},
                    className="arrow top-100 start-0"
                ),
                className=arrow_class
            ),
            dbc.CardHeader(
                [
                    html.Button(
                        [
                            html.Pre([f'{row["nom"]} {row["prenom"].title()} '], className="pb-0 mb-0", style={"font-size": "14px", "text-decoration": "none"}),
                            dbc.Badge(
                                [row['id'], html.Span([], className="visually-hidden")],
                                id="id-badge-front",
                                className=f"position-absolute bg-dark",
                                style={"fontSize": "8px", "transform": "translateX(-50%)"}
                            )
                        ],
                        id=btn_id,
                        className=f"btn btn-{color} btn-sm d-block fw-bold w-100 mb-2"
                    ),
                    html.Div(

                            kpis
                        ,
                        className="d-flex justify-content-center"
                    ),
                    html.Span(
                        html.Img(
                            [],
                            id={"type": "card-shield", "index": row['id']},
                            src="assets/img/shield_125.png",
                            height=25,
                            width=25,
                            style={"transform": "translateX(-50%)"},
                            className="shield"
                        ),
                        className=shield_class,
                        style={"zIndex": 3}
                    )
                ],
                className="p-3"
            ),
            card_content
        ],
        className="flip-card-front px-0",
        style=front_style
    )


def build_tile_back(row):

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
            dbc.Badge(
                row['uga'],
                id={"type": "uga-badge-back", "index": row["id"]},
                className="uga-badge position-absolute top-0 start-0 px-2 bg-white"
            ),
            dbc.Badge(
                row['spe'],
                id={"type": "spe-badge-back", "index": row["id"]},
                color=f"{doctor_colors[row['spe']]}",
                text_color="white",
                className="spe-badge my-1 position-absolute top-0 start-100"
            ),
            dbc.Badge(
                [row['cib'], html.Span([], className="visually-hidden")],
                id="cib-badge-back",
                className=f"position-absolute top-100 start-0 bg-{badge_color}",
                style={"fontSize": "13px", "transform": "translate(-50%, -50%)"}
            ),
            html.Span(
                html.Img(
                    [],
                    id={"type": "blue-arrow-btn-back", "index": row['id']},
                    src="assets/img/blue_turn.png",
                    height=25,
                    width=25,
                    style={"position": "absolute", "zIndex": "1", "transform": "translate(-75%, -50%) rotateY(180deg)"},
                    className="arrow top-100 start-100"
                )
            ),
            dbc.CardHeader(
                [
                    html.Button(
                        [
                            html.Pre(f'{row["nom"]} {row["prenom"].title()}', className="mb-0",
                                     style={"fontSize": "15px", "textDecoration": "none"}),

                        ],
                        id={"type": "modal-btn", "index": row['id']},
                        className=f"btn btn-{color} d-block fw-bold w-100"
                    )
                ],
                className="d-flex flex-column p-3"
            ),
            dbc.CardBody(
                [

                ]
            ),
            dbc.CardFooter(
                [

                ]
            )
        ],
        className="flip-card-back px-0 w-100",
        style={"backgroundColor": "#FFFFFF", "opacity": 1}
    )


def build_modal(row, is_open=False):

    return  dbc.Modal(
        [
            dbc.ModalHeader(
                [],
                id="modal-header"
            ),
            dbc.ModalBody(
                dbc.Row(
                    [
                        dbc.Col([build_tile_front(row, in_modal=True, need_form=True)], width=12, className="d-flex justify-content-center")
                    ],
                    style={"height": "475px"}
                ),
                id="modal-body",
            ),
            dbc.ModalFooter(
                [
                ],
                id="modal-footer"
            ),
        ],
        id={"type": "modal", "index": row['id']},
        centered=True,
        is_open=is_open
    )


def build_flip(row):

    return  html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            build_tile_front(row),
                            build_tile_back(row)

                        ],
                        className="flip-card-inner",
                    )
                ],
                className="flip-card p-0 col-lg-2",
            )
        ],
        className="row p-3 complete-card m-3 small",
    )

"""
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

"""


id_adr = join_id_adr()
(styles1, legend1) = discrete_background_color_bins(id_adr, n_bins=9, columns=["pvm"])
(styles2, legend2) = discrete_background_color_bins(id_adr, n_bins=9, columns=["pot"], colorscale="YlGn")
styles = styles1 + styles2

df = join_id_adr_cdb()
mean_lat = df['lat'].mean()
mean_lon = df['lon'].mean()

datatable_cols =[{"name": i.upper(), "id": i} for i in df.columns]


