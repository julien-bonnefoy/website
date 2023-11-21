from dash import html
import dash_leaflet as dl
from application.dash.biocodex.functions import mean_lat, mean_lon
import dash
from dash_extensions.javascript import Namespace, arrow_function
import dash_leaflet as dl
import dash_leaflet.express as dlx
import json
from flask import render_template
from application.dash.biocodex.functions import df

dash.register_page(__name__, path="/map")

data = df.to_dict('records')

def p_popup(pharmacy):
    return f"""
            <b>{pharmacy['nom']}</b>
            <br>{pharmacy["adr"]}
            <br>{pharmacy["cp"]} {pharmacy["ville"]} ({pharmacy["uga"]})
            <br>{pharmacy["tel"]}                         
        """
"""
<br>CA UL (CMA juin 23): {pharmacy["ca ul cma juin 23"]} (rang {pharmacy["rang ca uk"]})
<br>Ciblage DP:{pharmacy["ciblage dp"]} DSO:{pharmacy["ciblage dso"]} DM:{pharmacy["ciblage dm"]}   
"""

def c_popup(row):
    return render_template("partials/front.html", row=row)


def data_to_geojson(data):
    df_geojson = dlx.dicts_to_geojson(
        [{**c, **dict(popup=c_popup(c))} if c['spe'] != "" else {**c, **dict(popup=p_popup(c))} for c in data])
    with open(f'assets/df_geojson.json', 'w') as j:
        j.write(json.dumps(df_geojson).replace(": ", ":").replace(", ", ","))
    return df_geojson



ns = Namespace('dashExtensions','default')

ugas = ["75AUT", "75PAS", "75TRO", "75ELY", "75INV", "75GRE", "75VAU", "75MNP", "75PER", "75TER", "92LEV", "92NEU"]

with open("assets/uga_gpd.json", "r") as uga_json:
    uga_geojson = json.loads(uga_json.read())

sector_features = [
    uga_geojson["features"][i] for i in range(len(uga_geojson["features"])) if uga_geojson["features"][i]["properties"]["CODE_UGA"] in ugas
]
uga_geojson["features"] = sector_features

ugas_layer = dl.GeoJSON(
    data=uga_geojson,
    hideout=dict(selected=[]),
    filter=ns('uga_geojson_filter'),
    style=ns('uga_style_handle'),
    hoverStyle=arrow_function(dict(weight=3, color='red', dashArray='')),
    zoomToBounds=True,
    id="uga-geojson",
)

data_geojson = data_to_geojson(data)

data_layer = dl.GeoJSON(
    data=data_geojson,
    hideout=dict(ugas_selected=[], spes_selected=[], cib_selected=[], pvm_range=[]),
    filter=ns('geojson_filter'),
    zoomToBounds=True,
    pointToLayer=ns('cible_icon'),
    id="data-geojson"
)

layout = html.Div(
        [
            dl.Map(
                [
                   dl.LayersControl(
                        [
                            dl.BaseLayer(dl.TileLayer(), name="base", checked=True),
                            dl.Overlay(dl.LayerGroup(ugas_layer, id="ugas_layer_group"), name="ugas", checked=True),
                            dl.Overlay(dl.LayerGroup(data_layer, id="data_layer_group"), name="data", checked=True),
                            #dl.Overlay(dl.LayerGroup(target_layer, id="target_layer_group"), name="ciblés", checked=True),
                            #dl.Overlay(dl.LayerGroup(untarget_layer, id="untarget_layer_group"), name="non ciblés", checked=False),
                            #info
                        ]
                   ),
                    dl.FullScreenControl(),
                    dl.LocateControl(locateOptions={'enableHighAccuracy': True})
               ],
               center=(mean_lat, mean_lon),
               zoom=11,
               style={'height': '90vh', 'position': 'absolute', 'width': '90%'}
            )
        ],
        id='map'
    )
