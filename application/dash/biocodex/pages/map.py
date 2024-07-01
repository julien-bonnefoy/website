from dash import html
from application.dash.biocodex.functions import mean_lat, mean_lon, prepare_data, data_to_geojson, get_pharmas, pharmas_to_geojson
from application.dash.biocodex.functions import join_id_adr_cdb, make_engine
import dash
from dash_extensions.javascript import Namespace, arrow_function
import dash_leaflet as dl
import json


dash.register_page(__name__, path="/map")


df = prepare_data(join_id_adr_cdb(make_engine()))
data = df.to_dict('records')

ns = Namespace('dashExtensions','default')

with open("/var/www/website.julien-bonnefoy.dev/application/data/json/secteur_geojson.json", "r") as uga_json:
    uga_geojson = json.loads(uga_json.read())

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

pharmas = get_pharmas(make_engine())
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

mapp = dl.Map(
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
   style={'height': 'inherit', 'position': 'absolute', 'width': 'inherit'}
)

layout = html.Div(
        [
            mapp
        ],
        style={"height": "75vh","width": "75vw"},
        id="map-container",

    )
