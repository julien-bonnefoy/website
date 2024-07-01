import pandas as pd
from dash import Input, Output, State, MATCH, ClientsideFunction, clientside_callback
from application.dash.biocodex.functions import get_info, join_id_adr_cdb, build_flip, build_modal, unix_to_dt
from application.dash.biocodex.functions import make_engine
from application.dash.biocodex.pages.table import dashtable
import numpy as np
from psycopg2.extensions import register_adapter, AsIs
import re
import dash


register_adapter(np.int64, AsIs)


def init_callbacks(dashapp):

    dashapp.config.suppress_callback_exceptions = True

    dashapp.clientside_callback(
        ClientsideFunction(
            namespace='clientside',
            function_name='render_calendar'
        ),
        Output("calendar", "children"),
        Input("link2-calendar", "n_clicks"),
        Input("all-memory", "data")
    )


    # UGA & SPES SELECTION ==> UPDATE MEMORY
    @dashapp.callback(
        Output("memory", "data"),
        Input('uga-cl', 'value'),
        Input("spe-cl", "value"),
        Input("cib-cl", "value"),
        Input("pvm-slider", "value")
    )
    def filter(ugas_selected, spes_selected, cib_selected, pvm_range):
        data_df = join_id_adr_cdb(make_engine())
        data = data_df.query('uga in @ugas_selected') \
                      .query('spe1 in @spes_selected') \
                      .query('c24c2 in @cib_selected') \
                      .query('pvm > @pvm_range[0] and pvm < @pvm_range[1]')

        return data.to_dict('records')


    @dashapp.callback(
        Output("tabledash", "data"),
        Input('memory', 'data')
    )
    def update_table(data):
        if not data:
            data = join_id_adr_cdb(make_engine()).to_dict('records')

        for i in range(len(data)):
            row=data[i]
            for col in ['ddv', 'rdv']:
                if not pd.isnull(row[col]):
                    if type(row[col]) == int or type(row[col]) == float:
                        data[i][col] = unix_to_dt(row[col])

        return data


    @dashapp.callback(
        Output("tiles-content", "children"),
        Input("memory", "data")
    )
    def update_tiles(data):

        if not data:
            data = join_id_adr_cdb(make_engine()).to_dict('records')
        return [build_flip(d) for d in data]+[build_modal(d) for d in data]



    @dashapp.callback(
        Output("data-geojson", "hideout"),
        Output("pharma-geojson", "hideout"),
        Input("memory", "data"),
        State('uga-cl', 'value'),
        State("spe-cl", "value"),
        State("cib-cl", "value"),
        State("pvm-slider", "value")
    )
    def update_map(data, ugas_selected, spes_selected, cib_selected, pvm_range):
        data_hideout = dict(ugas_selected=ugas_selected, spes_selected=spes_selected, cib_selected=cib_selected, pvm_range=pvm_range)
        pharma_hideout = dict(ugas_selected=ugas_selected, cib_selected=cib_selected)
        return data_hideout, pharma_hideout


    @dashapp.callback(
        Output("table-container", "children"),
        Input("tabledash", "active_cell"),
        State("memory", "data")
    )
    def update_tabledash(act_cell, click_map, data):
        if not data:
            data = join_id_adr_cdb(make_engine()).to_dict('records')

        if act_cell:

            df = pd.DataFrame(data)
            row = df.loc[df['id']==act_cell["row_id"]].to_dict('records')[0]
            modal = build_modal(row, is_open=True)
            return [dashtable, modal]

        elif click_map:
            print(click_map['properties']['id'])

        else:
            return [dashtable]


    @dashapp.callback(
        Output("visdcc", "run"),
        Input("tiles-content", "children"),
        Input("map-container", "children"),
    )
    def run_js(tiles):
        return """
            const arrows = toArray(document.getElementsByClassName('arrow'));
            arrows.forEach( (arrow) => arrow.addEventListener('click', flipCard))
            const shields = toArray(document.getElementsByClassName('shield'));
            shields.forEach( (shield) => shield.addEventListener('click', toggleBodyCard))
        """

    @dashapp.callback(
        Output("page-container", "children"),
        Input("noms-dd", "value")
    )
    def modal_dd(nom_pre):
        data = join_id_adr_cdb(make_engine())
        if nom_pre is not None:
            reg = "([A-Z\s]+)\s(([A-Z]{1}[a-z\s]*)+)"
            s = re.search(reg, nom_pre)
            nom=s.group(1)
            pre=s.group(2)
            filter=(data['nom']==nom) & (data['pre']==pre)
            row=data.loc[filter].to_dict('records')[0]
            modal = build_modal(row, is_open=True)
            return [dash.page_container]+[modal]
        return [dash.page_container]


    @dashapp.callback(
        Output({'type': 'modal', 'index': MATCH }, "is_open"),
        Input({'type': 'modal-btn', 'index': MATCH}, "n_clicks"),
        Input({'type': 'submit', 'index': MATCH}, "n_clicks"),
        State({'type': 'modal', 'index': MATCH}, "is_open")
    )
    def toggle_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open


    @dashapp.callback(
        Output({'type': 'ddv-input', 'index': MATCH}, "value"),
        Input({'type': 'ddv-picker', 'index': MATCH}, "date")
    )
    def toggle_modal(d1):
        return d1

    @dashapp.callback(
        Output({'type': 'dpv-input', 'index': MATCH}, "value"),
        Input({'type': 'dpv-picker', 'index': MATCH}, "date")
    )
    def toggle_modal(d1):
        return d1


    # SIDEBAR TOGGLE
    @dashapp.callback(
        Output("sidebar-toggler", "className"),
        Output("sidebar", "className"),
        [Input("sidebar-toggler", "n_clicks")],
        [State("sidebar", "className")],
    )
    def toggle_classname(n, classname):
        if n and classname != "":
            return "btn-dark hamburger hamburger--elastic collapsed", ""
        return "btn-dark hamburger hamburger--elastic", "collapsed"


    # MAP CALLBACKS
    @dashapp.callback(
        Output("uga-geojson", "hideout"),
        Input("uga-cl", "value"),
        State("uga-geojson", "hideout"),
    )
    def ugas_select(ugas_selected, uga_hideout):
        uga_hideout["selected"] = ugas_selected
        return uga_hideout


    @dashapp.callback(
        Output("info", "children"),
        Input("uga-geojson", "hoverData"),
        State('memory', 'data')
    )
    def info_hover(feature, data):
        return get_info(pd.DataFrame(data), feature)
