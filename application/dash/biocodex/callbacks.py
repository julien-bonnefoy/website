import pandas as pd
from dash import Input, Output, State, ALL, MATCH
from application.dash.biocodex.functions import get_info, join_id_adr_cdb, build_flip, build_modal
from application.dash.biocodex.pages.table import dashtable
from application.dash.biocodex.pages.map import data_to_geojson
import numpy as np
from psycopg2.extensions import register_adapter, AsIs
import re
import dash


register_adapter(np.int64, AsIs)


def init_callbacks(dashapp):

    dashapp.config.suppress_callback_exceptions = True
    # UGA & SPES SELECTION ==> UPDATE MEMORY
    @dashapp.callback(
        Output("memory", "data"),
        Input('uga-cl', 'value'),
        Input("spe-cl", "value"),
        Input("cib-cl", "value"),
        Input("pvm-slider", "value")
    )
    def filter(ugas_selected, spes_selected, cib_selected, pvm_range):
        data_df = join_id_adr_cdb()
        data = data_df.query('uga in @ugas_selected') \
                      .query('spe in @spes_selected') \
                      .query('cib in @cib_selected') \
                      .query('pvm > @pvm_range[0] and pvm < @pvm_range[1]') \
                      .to_dict('records')
        return data

    @dashapp.callback(
        Output("tabledash", "data"),
        Input('memory', 'data')
    )
    def update_table(data):
        if not data:
            data = join_id_adr_cdb().to_dict('records')
        return data


    @dashapp.callback(
        Output("tiles-content", "children"),
        Input("memory", "data")
    )
    def update_tiles(data):

        if not data:
            data = join_id_adr_cdb().to_dict('records')
        return [build_flip(d) for d in data]+[build_modal(d) for d in data]


    @dashapp.callback(
        Output("data-geojson", "hideout"),
        Input("memory", "data"),
        State('uga-cl', 'value'),
        State("spe-cl", "value"),
        State("cib-cl", "value"),
        State("pvm-slider", "value")
    )
    def update_map(data, ugas_selected, spes_selected, cib_selected, pvm_range):

        if not data:
            data = join_id_adr_cdb().to_dict('records')
        # print(data_to_geojson(data))
        return dict(ugas_selected=ugas_selected, spes_selected=spes_selected, cib_selected=cib_selected, pvm_range=pvm_range)



    @dashapp.callback(
        Output("table-container", "children"),
        Input("tabledash", "active_cell"),
        State("memory", "data")
    )
    def update_tabledash(act_cell, data):
        if not data:
            data = join_id_adr_cdb().to_dict('records')

        if act_cell:
            df = pd.DataFrame(data)
            row = df.loc[df['id']==act_cell["row_id"]].to_dict('records')[0]
            modal = build_modal(row, is_open=True)
            return [dashtable, modal]
        else:
            return [dashtable]

    @dashapp.callback(
        Output("visdcc", "run"),
        Input("tiles-content", "children")
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
        data = join_id_adr_cdb()
        if nom_pre is not None:
            reg = "([A-Z\s]+)\s(([A-Z]{1}[a-z\s]*)+)"
            s = re.search(reg, nom_pre)
            nom=s.group(1)
            pre=s.group(2)
            filter=(data['nom']==nom) & (data['prenom']==pre)
            row=data.loc[filter].to_dict('records')[0]
            modal = build_modal(row, is_open=True)
            return [dash.page_container]+[modal]
        return [dash.page_container]

    @dashapp.callback(
        Output({'type': 'modal', 'index': MATCH }, "is_open"),
        Input({'type': 'modal-open', 'index': MATCH}, "n_clicks"),
        # Input({'type': 'modal-close', 'index': MATCH}, "n_clicks"),
        Input({'type': 'submit', 'index': MATCH}, "n_clicks"),
        State({'type': 'modal', 'index': MATCH}, "is_open"),
        prevent_initial_call=True
    )
    def toggle_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open

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
        Output("pharma-geojson", "hideout"),
        Input("uga-cl", "value"),
        State("pharma-geojson", "hideout")
    )
    def pharma_select(ugas_selected, pharma_hideout):
        pharma_hideout["ugas_selected"] = ugas_selected
        return pharma_hideout

    @dashapp.callback(
        Output("target-geojson", "hideout"),
        Input("uga-cl", "value"),
        Input("spe-cl", "value"),
        State("target-geojson", "hideout")
    )
    def target_select(ugas_selected, spes_selected, target_hideout):
        target_hideout["ugas_selected"] = ugas_selected
        target_hideout["spes_selected"] = spes_selected
        return target_hideout

    @dashapp.callback(
        Output("untarget-geojson", "hideout"),
        Input("uga-cl", "value"),
        Input("spe-cl", "value"),
        State("untarget-geojson", "hideout")
    )
    def untarget_select(ugas_selected, spes_selected, untarget_hideout):
        untarget_hideout["ugas_selected"] = ugas_selected
        untarget_hideout["spes_selected"] = spes_selected
        return untarget_hideout

    @dashapp.callback(
        Output("info", "children"),
        Input("uga-geojson", "hoverData"),
        State('memory', 'data')
    )
    def info_hover(feature, data):
        return get_info(pd.DataFrame(data), feature)
