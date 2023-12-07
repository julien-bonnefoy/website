from dash import html
from application.dash.biocodex.functions import mean_lat, mean_lon, prepare_data, data_to_geojson, get_pharmas, pharmas_to_geojson
from application.dash.biocodex.functions import join_id_adr_cdb
import dash
from dash_extensions.javascript import Namespace, arrow_function
import dash_leaflet as dl
import json


dash.register_page(__name__, path="/map")


df = prepare_data(join_id_adr_cdb())
data = df.to_dict('records')


ns = Namespace('dashExtensions','default')

ugas = ["75AUT", "75PAS", "75TRO", "75ELY", "75INV", "75GRE", "75VAU", "75MNP", "75PER", "75TER", "92LEV", "92NEU"]

with open("/home/julien/website/application/dash/assets/uga_gpd.json", "r") as uga_json:
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
    zoomToBoundsOnClick=True,
    pointToLayer=ns('cible_icon'),
    id="data-geojson"
)

pharmas = get_pharmas()
pharma_geojson = pharmas_to_geojson(pharmas.to_dict('records'))

pharma_layer = dl.GeoJSON(
    data=pharma_geojson,
    hideout=dict(ugas_selected=[], cib_selected=[]),
    filter=ns('pharmas_filter'),
    zoomToBounds=True,
    zoomToBoundsOnClick=True,
    pointToLayer=ns('pharmas_icon'),
    id="pharma-geojson"
)

layout = html.Div(
        [
            dl.Map(
                [
                   dl.LayersControl(
                        [
                            dl.BaseLayer(dl.TileLayer(), name="base", checked=True),
                            dl.Overlay(ugas_layer, name="ugas", checked=True),
                            dl.Overlay(data_layer, name="data", checked=True),
                            dl.Overlay(pharma_layer, name="pharmacies", checked=True)
                            #dl.Overlay(dl.LayerGroup(untarget_layer, id="untarget_layer_group"), name="non ciblés", checked=False),
                            #info
                        ]
                   ),
                    dl.FullScreenControl(),
                    dl.LocateControl(locateOptions={'enableHighAccuracy': True})
               ],
               id='map',
               center=(mean_lat, mean_lon),
               zoom=11,
               style={'height': '90vh', 'position': 'absolute', 'width': 'calc(100% - 6.5rem)'}
            )
        ]
    )
