from sqlalchemy import create_engine
from dash import html
from dash_extensions.javascript import Namespace, arrow_function
from application.dash.biocodex.functions import get_info
import dash_leaflet as dl
import os
from application.config import basedir
from dotenv import load_dotenv
import json
import pandas as pd



load_dotenv(os.path.join(basedir, '.env'))
DATABASE_URL=os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://')
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    df = pd.read_sql('SELECT * FROM identities', con=conn)


ns = Namespace('dashExtensions','default')

ugas = ["75AUT", "75PAS", "75TRO", "75ELY", "75INV", "75GRE", "75VAU", "75MNP", "75PER", "75TER", "92LEV", "92NEU"]

with open("assets/uga_gpd.json", "r") as uga_json:
    uga_geojson = json.loads(uga_json.read())

sector_features = [
    uga_geojson["features"][i] for i in range(len(uga_geojson["features"])) if uga_geojson["features"][i]["properties"]["CODE_UGA"] in ugas
]
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
    hideout=dict(ugas_selected=[]),
    filter=ns('pharma_filter'),
    zoomToBounds=True,
    pointToLayer=ns('pharma_icon'),
    id="pharma-geojson"
)

target_layer = dl.GeoJSON(
    data=target_geojson,
    hideout=dict(ugas_selected=[], spes_selected=[]),
    filter=ns('geojson_filter'),
    zoomToBounds=True,
    pointToLayer=ns('cible_icon'),
    id="target-geojson"
)

untarget_layer = dl.GeoJSON(
    data=untarget_geojson,
    hideout=dict(ugas_selected=[], spes_selected=[]),
    filter=ns('geojson_filter'),
    zoomToBounds=True,
    pointToLayer=ns('cible_icon'),
    id="untarget-geojson"
)

info = html.Div(
    children=get_info(df),
    id="info",
    className="info",
    style={"position": "absolute", "bottom": "10px", "left": "10px", "zIndex": "1000"}
)