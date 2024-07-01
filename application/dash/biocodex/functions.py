from sqlalchemy import create_engine, func, extract
from sqlalchemy.orm import Session, sessionmaker
from application.dash.biocodex.models import Cdb, Connection, Identity, Adress, Pharmacy
import pandas as pd
from dash import html, dash_table, dcc
import dash_bootstrap_components as dbc
import dash_datetimepicker
from random import randint
import numpy as np
import os
from application.config import basedir
from dotenv import load_dotenv
from flask_wtf import csrf
from datetime import datetime
import dash_leaflet.express as dlx
from flask import render_template


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
doctors_bg = {
    'GY': 'c23 v',
    'MGY': 'c23 v',
    'SF': 'c23 v',
    'MG': 'c2 v',
    'GE': 'c3 v',
    'PE': 'c11 v',
    'PPSY': 'c27 v',
    'PSY': 'c27 v',
    'NE': 'c27 v'
}


def make_engine():

    load_dotenv(os.path.join(basedir, '.env'))
    DATABASE_URL = f'postgresql://{os.environ.get("USERNAME")}:{os.environ.get("PASSWORD")}@{os.environ.get("HOST")}:{os.environ.get("PORT")}/{os.environ.get("DATABASE")}'
    engine = create_engine(DATABASE_URL)

    return engine


def make_session(engine):

    Session = sessionmaker(bind=engine)

    return Session()


def p_popup(row):
    for col in ['ddv']:
        if not pd.isnull(row[col]):
            if type(row[col]) == int or type(row[col]) == float:
                row[col] = unix_to_dt(row[col])
            elif isinstance(row[col], pd.Timestamp):
                row[col] = row[col].strftime(format="%d/%m/%Y %H:%M")

    return render_template("partials/pharma.html", row=row)


def tiptool(item):
    return render_template("partials/tooltip.html", content=item['nom'])


def c_popup(row):
    for col in ['ddv', 'rdv']:
        if not pd.isnull(row[col]):

            if type(row[col]) == int or type(row[col]) == float:
                row[col] = unix_to_dt(row[col])
            elif isinstance(row[col], pd.Timestamp):
                row[col] = row[col].strftime(format="%d/%m/%Y %H:%M")
    return render_template("partials/front.html", row=row)


def data_to_geojson(data):
    df_geojson = dlx.dicts_to_geojson([{**c, **dict(popup=c_popup(c), tooltip=c['nom'])} for c in data])
    return df_geojson


def pharmas_to_geojson(pharmas_data):
    df_geojson = dlx.dicts_to_geojson(
        [{**c, **dict(popup=p_popup(c), tooltip=c['nom'])} for c in pharmas_data]
    )
    return df_geojson


def json_js_to_geojson(json_js_file):
    import json

    with open(f'assets/js/{json_js_file}.js') as dataFile:
        data = dataFile.read()

        obj = data[data.find('{'): data.rfind('}') + 1]

        geojson = json.loads(obj)

    with open(f'assets/{json_js_file}.json', 'w') as j:
        j.write(json.dumps(geojson).replace(": ", ":").replace(", ", ","))

    return geojson


def prepare_data(df):
    df['nv22'] = df['nv22'].fillna('')
    df['nv22'] = [int(nv) if nv != '' else '' for nv in df['nv22']]

    df['c24c1'] = df['c24c1'].fillna('HC')
    df['cib'] = [int(c) if c != 'HC' else 'HC' for c in df['c24c1']]

    df['rdv'] = ['\u2705' if pd.isnull(row['rdv']) == 0 else '' for i, row in df.iterrows()]

    df.sort_values(['uga', 'adr', 'spe1', 'pot', 'pvm'], ascending=[True, True, True, False, False], inplace=True)

    return df


def join_id_adr(engine):
    with Session(engine) as session:
        id_adr = pd.read_sql_query(
            sql=session.query(
                Connection.doc_id, Identity.nom, Identity.pre, Identity.spe1, Identity.spe2, Identity.pot, Identity.pvm,
                Identity.dec, Identity.c24c1, Identity.c24c2, Identity.c23c3, Identity.nv23, Identity.nv22, Identity.age,
                Identity.conv, Identity.lieux, Identity.mail, Identity.veeva_link, Identity.ameli_link,
                Adress.uga, Adress.eta, Adress.adr, Adress.cp, Adress.vil, Adress.tel, Adress.mul, Adress.lat, Adress.lon
            ).join(Identity).join(Adress).statement,
            con=engine
        )
        session.close()

    return id_adr


def join_id_cdb(engine):
    with Session(engine) as session:
        id_cdb = pd.read_sql_query(
            sql=session.query(
                Connection.doc_id, Identity.nom, Identity.pre, Identity.spe1, Identity.spe2, Identity.pot, Identity.pvm,
                Identity.dec, Identity.c24c1, Identity.c24c2, Identity.c23c3, Identity.nv23, Identity.nv22, Identity.age,
                Identity.conv, Identity.lieux, Identity.mail, Identity.veeva_link, Identity.ameli_link,
                extract("EPOCH", Cdb.ddv), Cdb.ddvs, Cdb.rdv, Cdb.mode, Cdb.com, Cdb.rec, Cdb.motif, Cdb.lun_m, Cdb.lun_a, Cdb.mar_m,
                Cdb.mar_a, Cdb.mer_m, Cdb.mer_a, Cdb.jeu_m, Cdb.jeu_a, Cdb.ven_m, Cdb.ven_a
            ).join(Identity).join(Cdb).statement,
            con=engine
        )
        session.close()

    return id_cdb


def join_id_adr_cdb(engine):
    with Session(engine) as session:
        id_adr_cdb = pd.read_sql(
            sql=session.query(
                Connection.doc_id, Identity.nom, Identity.pre, Identity.spe1, Identity.spe2, Identity.pot, Identity.pvm,
                Identity.dec, Identity.c24c1, Identity.c24c2, Identity.c23c3, Identity.nv23, Identity.nv22, Identity.age,
                Identity.conv, Identity.lieux, Identity.mail, Identity.veeva_link, Identity.ameli_link,
                Adress.uga, Adress.eta, Adress.adr, Adress.cp, Adress.vil, Adress.tel, Adress.mul, Adress.lat, Adress.lon,
                Cdb.ddv, Cdb.ddvs, Cdb.rdv, Cdb.mode, Cdb.com, Cdb.rec, Cdb.motif, Cdb.lun_m, Cdb.lun_a, Cdb.mar_m,
                Cdb.mar_a, Cdb.mer_m, Cdb.mer_a, Cdb.jeu_m, Cdb.jeu_a, Cdb.ven_m, Cdb.ven_a
            ).join(Identity).join(Adress).join(Cdb).statement,
            con=engine
        )
        session.close()
        id_adr_cdb.columns = [
            'id', 'nom', 'pre', 'spe1', 'spe2', 'pot', 'pvm', 'dec', 'c24c1', 'c24c2', 'c23c3', 'nv23', 'nv22',
            'age', 'conv', 'lieux', 'mail', 'veeva_link', 'ameli_link',
            'uga', 'eta', 'adr', 'cp', 'vil', 'tel', 'mul', 'lat', 'lon',
            'ddv', 'ddvs', 'rdv', 'mode', 'com', 'rec', 'motif',
            'lun_m', 'lun_a', 'mar_m', 'mar_a', 'mer_m', 'mer_a', 'jeu_m', 'jeu_a',
            'ven_m', 'ven_a'
        ]

        df = prepare_data(id_adr_cdb)

    return df


def get_pharmas(engine):

    index_col = [
            'id', 'nom', 'adr', 'cp', 'vil', 'tel',
            'c24c1', 'cib_dp', 'cib_dso',  'nv22', 'ddv', 'ddvs', 'rdv',
            "circ_ca_cma_fev23", "ul_ca_cma_fev23", "ul_ca_rank_fev23",
            "circ_ca_cma_juin23", "ul_ca_cma_juin23", "ul_ca_rank_juin23",
            "circ_ca_cma_sep23", "ul_ca_cma_sep23", "ul_ca_rank_sep23",
            "circ_ca_cma_fev24", "ul_ca_cma_fev24", "ul_ca_rank_fev24",
            "gpt", "contrat_23",  "com", 'lat', 'lon'
        ]

    with Session(engine) as session:
        pharmas = pd.read_sql_query(
            sql=session.query(
                Pharmacy.id, Pharmacy.nom, Pharmacy.adr, Pharmacy.cp, Pharmacy.vil, Pharmacy.tel,
                Pharmacy.c24c1, Pharmacy.cib_dp, Pharmacy.cib_dso, Pharmacy.nv22, Pharmacy.ddv, Pharmacy.ddvs, Pharmacy.rdv,
                Pharmacy.circ_ca_cma_fev23, Pharmacy.ul_ca_cma_fev23, Pharmacy.ul_ca_rank_fev23,
                Pharmacy.circ_ca_cma_juin23, Pharmacy.ul_ca_cma_juin23, Pharmacy.ul_ca_rank_juin23,
                Pharmacy.circ_ca_cma_sep23, Pharmacy.ul_ca_cma_sep23,Pharmacy.ul_ca_rank_sep23,
                Pharmacy.circ_ca_cma_fev24, Pharmacy.ul_ca_cma_fev24,Pharmacy.ul_ca_rank_fev24,
                Pharmacy.gpt, Pharmacy.contrat_23, Pharmacy.com, Pharmacy.lat, Pharmacy.lon
            ).select_from(Pharmacy).statement,
            con=engine
        )

        session.close()

    pharmas.columns = index_col

    return pharmas


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
    compo = df.pivot_table(values="nom", index=["uga", "spe1"], columns="cib", aggfunc='count').fillna(0).astype(int)
    compo = compo[[2, 3, 4, 0]]
    compo.columns = ["2x", "3x", "4x", "non ciblé"]
    compo.index.name = None
    new_index = pd.MultiIndex.from_product([
        ugas,
        spes
    ], names=["uga", "spe1"])
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
                'if': {'column_id': 'spe1'},
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
            [html.Td(df.iloc[i, j], id='{}_{}_{}'.format(id, i, j)) for j in range(len(df.columns))]
        ) for i in range(len(df))]
    )
    return [Thead, Tbody]


def build_data(row, el, disabled):
    return html.Div(
        [
            dbc.FormFloating(
                [
                    dbc.Input(disabled=disabled, value=row[el], name=el, size="sm", className="pt-3")
                ],
                className="border-3 border-info col-12 px-0"
            )
        ], className="d-flex"
    )


def build_calendar(row, in_modal=False):
    disabled = True
    if in_modal:
        disabled = False

    return html.Div(
        [
            html.Thead(
                [
                    html.Tr(
                        [
                            html.Th(), html.Th('MATIN'), html.Th('AP. MIDI')
                        ]
                    )
                ]
            ),
            html.Tbody(
                [
                    html.Tr(
                        [
                            html.Td(children="LUNDI"),
                            html.Td(children=build_data(row, 'lun_m', disabled), id='<built-in function id>_0_0'),
                            html.Td(children=build_data(row, 'lun_a', disabled), id='<built-in function id>_0_1')
                        ]
                    ),
                    html.Tr(
                        [
                            html.Td(children="MARDI"),
                            html.Td(children=build_data(row, 'mar_m', disabled), id='<built-in function id>_1_0'),
                            html.Td(children=build_data(row, 'mar_a', disabled), id='<built-in function id>_1_1')
                        ]
                    ),
                    html.Tr(
                        [
                            html.Td(children="MERCREDI"),
                            html.Td(children=build_data(row, 'mer_m', disabled), id='<built-in function id>_2_0'),
                            html.Td(children=build_data(row, 'mer_a', disabled), id='<built-in function id>_2_1')
                        ]
                    ),
                    html.Tr(
                        [
                            html.Td(children="JEUDI"),
                            html.Td(children=build_data(row, 'jeu_m', disabled), id='<built-in function id>_3_0'),
                            html.Td(children=build_data(row, 'jeu_a', disabled), id='<built-in function id>_3_1')
                        ]
                    ),
                    html.Tr(
                        [
                            html.Td(children="VENDREDI"),
                            html.Td(children=build_data(row, 'ven_m', disabled), id='<built-in function id>_4_0'),
                            html.Td(children=build_data(row, 'ven_a', disabled), id='<built-in function id>_4_1')
                        ]
                    )
                ]
            )
        ],
        style={"font-size": "12px"}
    )


def build_tile_front(row, in_modal=False, need_form=False):

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

    if not pd.isnull(row['rdv']):
        if type(row['rdv']) == int or type(row['rdv']) == float:
            dpv = unix_to_dt(row['rdv'])
            if row['rdv'] < now.timestamp():
                color = 'danger'
            elif row['rdv'] > now.timestamp():
                color = 'success'

    badge_color = "secondary"
    if not pd.isnull(row['ddv']):
        if type(row['ddv']) == int or type(row['ddv']) == float:
            ddv = unix_to_dt(row['ddv'])
            if row['ddv'] >= int(pd.to_datetime("01/08/2023 00:00", dayfirst=True).timestamp()):
                badge_color = 'success'
                color = "success"

    btn_id = {"type": "modal-btn", "index": row['id']}
    sub_id = {"type": "submit", "index": row['id']}
    cal_btn_id = {"type": "cal-modal-btn", "index": row['id']}
    form_id = f"form-{row['id']}"
    arrow_class = "d-block"
    shield_class = "d-block p-0 border-0"
    save_btn_style = {"display": "none"}
    disabled = True
    hide = "hide"
    front_style = {"backgroundColor": "#FFFFFF", "opacity": 1}
    calendar = build_calendar(row)
    if in_modal:
        btn_id = f"btn-{row['id']}"
        sub_id = f"sub-{row['id']}"
        cal_btn_id = f"cal-btn-{row['id']}"
        form_id = {"type": "form", "index": row['id']}
        arrow_class = shield_class = "d-none"
        save_btn_style = {"display": "block"}
        disabled = False
        hide = ""
        front_style = {"backgroundColor": "#FFFFFF", "opacity": 1, "width": "330px"}
        calendar = build_calendar(row, in_modal=True)

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
            dbc.Input(disabled=True, value=row['nv22'], id=f"nv22-input", size="sm",
                      className="pt-3 fw-bolder bg-light"),
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
    if row["spe1"] == "PSY" or row["spe1"] == "PPSY":
        kpis = [potentiel, pvm, nv22, decile]
    else:
        kpis = [potentiel, pvm, nv22]

    rdint = randint(1,28)

    cheader = dbc.CardHeader(
        [
            html.Button(
                [
                    html.Pre([f'{row["nom"]} {row["pre"].title()} '], className="pb-0 mb-0",
                             style={"font-size": "14px", "text-decoration": "none", "letter-spacing": "-1px"}),
                    dbc.Badge(
                        [row['age'], html.Span([], className="visually-hidden")],
                        id="id-badge-front",
                        className=f"position-absolute bg-dark",
                        style={"fontSize": "10px", "transform": "translateX(-50%)", "letter-spacing": "2px", "top": "20px", "left":"245px", "padding": "5px"}
                    )
                ],
                id=btn_id,
                className=f"btn btn-{color} btn-sm d-block fw-bold w-100 mb-2"
            ),
            html.Div(
                kpis, className="d-flex justify-content-center"
            )
        ],
        className=f"p-3 {doctors_bg[row['spe1'].upper()]}"
    )

    cbody = dbc.CardBody(
        [
            html.Div(
                [
                    dbc.FormFloating(
                        [
                            dbc.Input(disabled=disabled, value=row['adr'], name="adr", size="sm", className="pt-3"),
                            dbc.Label('ADRESSE', size="sm", className="px-1 py-2 bg-transparent"),
                        ],
                        className="border-3 border-info col-12 px-0"
                    )
                ], className="d-flex"
            ),
            html.Div([
                dbc.Badge(dbc.Input(disabled=disabled, value=row['tel'], name="tel", size="sm",
                                    className="text-bold my-2 col-5", style={"font-size": "12px"}),
                          color="#FFFFFF", style={"opacity": .5, "color": "#000080"}),
                dbc.FormFloating([
                    dbc.Input(disabled=disabled, value=row['cp'], name="cp", size="sm", className="pt-3"),
                    dbc.Label('CP', size="sm", className="px-1 py-2 bg-transparent")
                ], className="border-3 border-info col-3 px-0"),
                dbc.FormFloating([
                    dbc.Input(disabled=disabled, value=row['vil'], name="ville", size="sm", className="pt-3",
                              style={"font-size": "11px", "overflow-x": "hidden"}),
                    dbc.Label('VILLE', size="sm", className="px-1 py-2 bg-transparent")
                ], className="border-3 border-info col-4 px-0"),
            ], className="d-flex"),
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
                    dbc.Input(disabled=disabled, value=row['motif'], name="pk", size="sm",
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
            ], className="d-flex"),
            html.Hr(),
            calendar
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
                        dcc.Input(id={"type": "ddv-input", "index": row['id']}, disabled=disabled, value=ddv, name="ddv", size="sm", className="pt-4 pb-0", type="hidden"),
                        dbc.Label('DDV', size="sm", className="px-1 py-2 bg-transparent", style={"font-size": "10px", "color": "#000080", "transform": "translateY(-30%)"}),
                        dash_datetimepicker.DashDatetimepickerSingle(
                           id={"type": "ddv-picker", "index": row['id']},
                           locale="fr",
                           date=ddv
                        ),
                    ], className="ms-auto w-50"),

                    dbc.FormFloating([
                        dbc.Input(id={"type": "dpv-input", "index": row['id']}, disabled=disabled, value=dpv, name="rdv", size="sm", className="pt-4 pb-0", type="hidden"),
                        dbc.Label('rdv', size="sm", className="px-1 py-2 bg-transparent", style={"color": "#000080", "transform": "translateY(-30%)"}),
                        dash_datetimepicker.DashDatetimepickerSingle(
                            id={"type": "dpv-picker", "index": row['id']},
                            locale="fr",
                            date=dpv
                        ),
                    ], className="w-50")
                ],
                className="d-flex"
            )
        ],
        className=f"small p-3 {doctors_bg[row['spe1'].upper()]}"
    )

    input = dbc.Input(
        id=sub_id,
        value="SAVE & CLOSE",
        className="btn btn-xl mx-auto",
        type="submit",
        style=save_btn_style
    )



    pharma_form = html.Form(
        [
            cheader,
            cbody,
            cfooter,
            input
        ],
        id=form_id,
        method='post',
        action=f'/dash/biocodex/pharma/{row["id"]}'
    )

    card_content = html.Div([cheader, cbody, cfooter, input])

    if need_form:
        token = dbc.Input(
            id="csrf_token",
            name="csrf_token",
            type="hidden",
            value=csrf.generate_csrf()
        )

        pds_form = html.Form(
            [
                token,
                cheader,
                cbody,
                cfooter,
                input
            ],
            id=form_id,
            method='post',
            action=f'/dash/biocodex/pds/{row["id"]}'
        )

        card_content = pds_form

    return dbc.Card(
        [
            dbc.Badge(
                row['uga'],
                id={"type": "uga-badge-front", "index": row["id"]},
                className="uga-badge position-absolute top-0 start-100  bg-white"
            ),
            dbc.Badge(
                row['spe1'],
                id={"type": "spe-badge-front", "index": row["id"]},
                color=f"{doctor_colors[row['spe1']]}",
                className="spe-badge my-1 position-absolute top-0 start-0"
            ),
            dbc.Badge(
                [row['c24c1'], html.Span([], className="visually-hidden")],
                id="cib-badge-front",
                className=f"position-absolute top-100 start-100 bg-{badge_color}",
                style={"fontSize": "13px", "transform": "translate(-50%, -50%)"}
            ),
            html.Span(
                html.Img(
                    [],
                    id={"type": "blue-arrow-btn-front", "index": row['id']},
                    src="../../../static/img/blue_turn.png",
                    height=25,
                    width=25,
                    style={"position": "absolute", "zIndex": 3, "transform": "translate(-25%, -50%)"},
                    className="arrow top-100 start-0"
                ),
                className=arrow_class
            ),
            html.Span(
                html.Img(
                    [],
                    id={"type": "card-shield", "index": row['id']},
                    src="../../../static/img/shield_125.png",
                    height=25,
                    width=25,
                    style={"position": "absolute", "zIndex": 3, "transform": "translate(130px, -55px)"},
                    className="shield"
                ),
                className=shield_class,
                style={"zIndex": 3}
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

    if type(row['rdv']) == int:
        dpv = unix_to_dt(row['rdv'])
        if row['rdv'] < now.timestamp():
            color = 'danger'
        elif row['rdv'] > now.timestamp():
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
                row['spe1'],
                id={"type": "spe-badge-back", "index": row["id"]},
                color=f"{doctor_colors[row['spe1']]}",
                text_color="white",
                className="spe-badge my-1 position-absolute",
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
                    src="../../../static/img/blue_turn.png",
                    height=25,
                    width=25,
                    style={"position": "absolute", "zIndex": "1", "transform": "translate(-75%, -50%) rotateY(180deg)"},
                    className="arrow top-100 start-100"
                )
            ),
            dbc.CardHeader(
                [
                    html.Pre(f'{row["nom"]} {row["pre"].title()}', className="mb-0",
                                 style={"fontSize": "15px", "textDecoration": "none"})
                ],
                className="d-flex flex-column p-3"
            ),
            dbc.CardBody(
                [

                ],
                className='hide'
            ),
            dbc.CardFooter(
                [

                ],
                className="small"
            )
        ],
        className="flip-card-back px-0 w-100",
        style={"backgroundColor": "#FFFFFF", "opacity": 1}
    )


def build_modal(row, is_open=False, in_modal=True, need_form=True):

    return dbc.Modal(
        [
            dbc.ModalHeader(
                [],
                id="modal-header"
            ),
            dbc.ModalBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    build_tile_front(row, in_modal=in_modal, need_form=need_form)
                                ],
                                width=12,
                                className="d-flex justify-content-center"
                            )
                        ],
                        style={"height": "475px"}
                    )
                ],
                id="modal-body"
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
    return html.Div(
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

id_adr = join_id_adr(make_engine())
(styles1, legend1) = discrete_background_color_bins(id_adr, n_bins=9, columns=["pvm"])
(styles2, legend2) = discrete_background_color_bins(id_adr, n_bins=9, columns=["pot"], colorscale="YlGn")
styles = styles1 + styles2

df = join_id_adr_cdb(make_engine())
mean_lat = df['lat'].mean()
mean_lon = df['lon'].mean()

datatable_cols = [{"name": i.upper(), "id": i, "hideable": True} for i in df.columns]
df = prepare_data(df)


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
    connection = Connection.query.filter(Connection.id==conn_id).first()
    doctor = connection.doc
    prenom = doctor.prenom.lower().replace(' ', '-')
    nom = doctor.nom.lower().replace(' ', '-')
    spe=doctors_spes[doctor.spe]
    adress=connection.adr
    ville = adress.ville.lower()
    return f"https://www.doctolib.fr/{spe}/{ville}/{prenom}-{nom}"

"""


