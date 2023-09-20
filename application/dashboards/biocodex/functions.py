from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from application.dashboards.biocodex.models import Identity, Adress, Cdb, Connections
import pandas as pd
from dash import html, dash_table
import dash_bootstrap_components as dbc
from flask import url_for
from dash_extensions.javascript import Namespace, arrow_function
import numpy as np
import json
import dash_leaflet as dl
import os
from application.config import basedir
from dotenv import load_dotenv

load_dotenv(os.path.join(basedir, '.env'))
DATABASE_URL=os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://')
engine = create_engine(DATABASE_URL)


def join_id_adr():

    with Session(engine) as session:
        id_adr = pd.read_sql_query(
            sql=session.query(
                Connections.doc_id, Identity.nom, Identity.prenom, Identity.spe, Identity.pot, Identity.pvm,
                Identity.nv2022, Identity.ciblage, Adress.etablissement, Adress.uga, Adress.adresse, Adress.cp, Adress.ville, Adress.tel,
                Adress.lat, Adress.lon
            ).join(Identity).join(Adress).statement,
            con=engine
        )
        session.close()
        id_adr.columns = [
            'id', 'nom', 'prenom', 'spe', 'pot', 'pvm', 'nv2022', 'ciblage', 'etablissement',
            'uga', 'adresse', 'cp', 'ville', 'tel', 'lat', 'lon'
        ]
    return id_adr


def join_id_cdb():

    with Session(engine) as session:
        id_cdb = pd.read_sql_query(
            sql=session.query(
                Connections.doc_id, Identity.nom, Identity.prenom, Identity.spe, Identity.pot, Identity.pvm,
                Identity.nv2022,
                Cdb.lun_mat, Cdb.lun_am, Cdb.mar_mat, Cdb.mar_am, Cdb.mer_mat, Cdb.mer_am, Cdb.jeu_mat, Cdb.jeu_am,
                Cdb.ven_mat, Cdb.ven_am, Cdb.ddv
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
                Identity.nv2022, Identity.ciblage,
                Adress.etablissement, Adress.uga, Adress.adresse, Adress.cp, Adress.ville, Adress.tel, Adress.lat, Adress.lon,
                Cdb.mode, Cdb.commentaire, Cdb.lun_mat, Cdb.lun_am, Cdb.mar_mat, Cdb.mar_am, Cdb.mer_mat, Cdb.mer_am, Cdb.jeu_mat, Cdb.jeu_am,
                Cdb.ven_mat, Cdb.ven_am, Cdb.ddv
            ).join(Identity).join(Adress).join(Cdb).statement,
            con=engine
        )
        session.close()

    return id_adr_cdb


def discrete_background_color_bins(df, n_bins=5, columns='all', colorscale="Blues"):
    import colorlover
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    if columns == 'all':
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


id_adr = join_id_adr()

(styles1, legend1) = discrete_background_color_bins(id_adr, n_bins=9, columns=["pvm"])
(styles2, legend2) = discrete_background_color_bins(id_adr, n_bins=9, columns=["pot"], colorscale="YlGn")
styles = styles1 + styles2

df = join_id_adr_cdb()

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

ciblage_options = [
    {"label": "Non ciblé", "value": 0},
    {"label": "1", "value": 1},
    {"label": "2", "value": 2},
    {"label": "3", "value": 3},
    {"label": "4", "value": 4}
]

datatable_cols =[{"name": i.upper(), "id": i} for i in df.columns]

def build_one(row):

    return dbc.Col(
    [
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.Div(
                            [
                                html.Div(html.Img(width=32, height=32, src=url_for("static", filename=f"img/{row['spe']}.jpg"), className="avatar-md rounded-circle img-thumbnail"))
                            ]
                            , className="d-flex align-items-center"
                        ),
                        html.Div(
                            [
                                html.P(
                                    [
                                        html.A([row["nom"],row["prenom"].title()], className="text-dark", href=f"/dash/biocodex/table/{row['doc_id']}", style={"font-size": 10})
                                    ]
                                ),
                                html.Span(

                                        row["spe"]
                                    ,
                                    className="badge badge-success mb-0"
                                )
                            ],
                            className="flex-1 ms-3"),
                        html.Div([]),
                    ]
                )
            ]
        )
    ],
        className="col-xl-2 col-sm-6",
)

mean_lat = df['lat'].mean()
mean_lon = df['lon'].mean()


def get_compo(df):
    idx = pd.IndexSlice
    compo = df.pivot_table(values="nom", index=["uga", "spe"], columns="ciblage", aggfunc='count').fillna(0).astype(int)
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


def get_info(feature=None):
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

ugas = ["75AUT", "75PAS", "75TRO", "75ELY", "75INV", "75GRE", "75VAU", "75MNP", "75PER", "75TER", "92LEV", "92NEU"]
spes = ["GY", "MG-GY", "SF", "MG", "GE", "PE", "PE-PSY", "PSY", "NE"]

ns = Namespace('dashExtensions','default')

with open("assets/uga_gpd.json", "r") as uga_json:
    uga_geojson = json.loads(uga_json.read())

sector_features = [uga_geojson["features"][i] for i in range(len(uga_geojson["features"])) if
                   uga_geojson["features"][i]["properties"]["CODE_UGA"] in ugas]
uga_geojson["features"] = sector_features

with open("assets/pharmas_geojson.json", "r") as pharma_json:
    pharma_geojson = json.loads(pharma_json.read())

with open("assets/target_geojson.json", "r") as cible_json:
    target_geojson = json.loads(cible_json.read())

with open("assets/untarget_geojson.json", "r") as cible_json:
    untarget_geojson = json.loads(cible_json.read())

ugas_layer = dl.GeoJSON(
    data=uga_geojson,
    hideout=dict(selected=[]),
    filter=ns('uga_geojson_filter'),
    style=ns('uga_style_handle'),
    hoverStyle=arrow_function(dict(weight=3, color='red', dashArray='')),
    zoomToBounds=True,
    id="uga-geojson",
)

pharmas_layer = dl.GeoJSON(
    data=pharma_geojson,
    hideout=dict(selected=[]),
    filter=ns('geojson_filter'),
    zoomToBounds=True,
    pointToLayer=ns('pharma_icon'),
    id="pharma-geojson"
)

target_layer = dl.GeoJSON(
    data=target_geojson,
    hideout=dict(selected=[]),
    filter=ns('geojson_filter'),
    pointToLayer=ns('cible_icon'),
    cluster=True,
    id="target-geojson"
)

untarget_layer = dl.GeoJSON(
    data=untarget_geojson,
    hideout=dict(selected=[]),
    filter=ns('geojson_filter'),
    zoomToBounds=True,
    pointToLayer=ns('cible_icon'),
    id="untarget-geojson"
)

info = html.Div(
    children=get_info(),
    id="info",
    className="info",
    style={"position": "absolute", "bottom": "10px", "left": "10px", "zIndex": "1000"}
)