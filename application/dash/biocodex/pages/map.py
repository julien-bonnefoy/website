from dash import html
from application.dash.biocodex.map import ugas_layer, pharmas_layer, target_layer, untarget_layer, info
import dash_leaflet as dl
from application.dash.biocodex.functions import mean_lat, mean_lon
import dash

dash.register_page(__name__, path="/map")

layout = html.Div(
        [
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
        ],
        id='map'
    )
