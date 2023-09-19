from dash import Dash, html, dcc, Input, Output, dash_table, callback, State, ClientsideFunction
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import collections
import pandas as pd
import json
import random
from app.dashboards.biocodex.functions import join_id_adr_cdb, spe_options, uga_options, ciblage_options, datatable_cols, styles, build_one
from dash_extensions.javascript import assign, arrow_function, Namespace
import dash_leaflet as dl
import dash_leaflet.express as dlx

ugas = ["75AUT", "75PAS", "75TRO", "75INV", "75GRE", "75VAU", "75MNP", "75PER", "75TER", "92LEV", "92NEU"]
spes = ["GY", "MG-GY", "SF", "MG", "GE", "PE", "PE-PSY", "PSY", "NE"]
df = join_id_adr_cdb()

cible = df[df["ciblage"]!=0].copy()
cible["tel"] = [tel[:2]+" "+tel[2:4]+" "+tel[4:6]+" "+tel[6:8]+" "+tel[8:10] for tel in cible["tel"]]

with open("assets/uga_gpd.json", "r") as uga_json:
    uga_geojson = json.loads(uga_json.read())

sector_features = [uga_geojson["features"][i] for i in range(len(uga_geojson["features"])) if uga_geojson["features"][i]["properties"]["CODE_UGA"] in ugas]
uga_geojson["features"] = sector_features

with open("assets/pharmas_geojson.json", "r") as pharma_json:
    pharma_geojson = json.loads(pharma_json.read())

ns = Namespace('dashExtensions', 'default')

ugas_layer = dl.GeoJSON(
    data=uga_geojson,
    hideout=dict(selected=[]),
    filter=ns('uga_geojson_filter'),
    style=ns('uga_style_handle'),
    hoverStyle=arrow_function(dict(weight=5, color='#666', dashArray='')),
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

external_scripts = ["js/leaflet.extra-markers.min.js"]
external_stylesheets = [dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME, "css/leaflet.extra-markers.min.css"]

app = Dash(external_scripts=external_scripts, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        dcc.Checklist(id="uga-cl", value=ugas, options=[{"value": uga, "label": uga} for uga in ugas], inline=True),
        dl.Map(
            [
                dl.LayersControl(
                    [
                        dl.BaseLayer(dl.TileLayer(), name="base", checked=True),
                        dl.Overlay(dl.LayerGroup(ugas_layer, id="ugas_layer_group"), name="ugas", checked=True),
                        dl.Overlay(dl.LayerGroup(pharmas_layer, id="pharmas_layer_group"), name="pharmas",
                                   checked=True),
                    ]
                )

            ],
            center=(cible["lat"].mean(), cible["lon"].mean()),
            zoom=12,
            style={'height': '90vh'}
        )
    ])


@app.callback(
    Output("uga-geojson", "hideout"),
    Input("uga-cl", "value"),
    State("uga-geojson", "hideout"),
)
def toggle_select(uga_selected, uga_hideout):
    uga_hideout["selected"] = uga_selected
    return uga_hideout


@app.callback(
    Output("pharma-geojson", "hideout"),
    Input("uga-cl", "value"),
    State("pharma-geojson", "hideout")
)
def toggle_select(uga_selected, pharma_hideout):
    pharma_hideout["selected"] = uga_selected
    return pharma_hideout

if __name__ == "main":
    app.run_server(debug=True)