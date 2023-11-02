import pandas as pd
from dash import Input, Output, State, html, dcc, DiskcacheManager
from application.dash.biocodex.functions import build_flip, get_info, join_id_adr_cdb, doctor_colors
from application.pds.controllers import retrieve_pds_ctrlr
from application.pds.forms import CdbForm
import numpy as np
from psycopg2.extensions import register_adapter, AsIs
import re
from flask import render_template




reg=re.compile("[0-9]+")
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
    def filter(ugas_selected, spe_selected, cib_selected, pvm_range):
        data_df = join_id_adr_cdb()
        data = data_df.query('uga in @ugas_selected') \
                      .query('spe in @spe_selected') \
                      .query('cib in @cib_selected') \
                      .query('pvm > @pvm_range[0] and pvm < @pvm_range[1]') \
                      .to_dict('records')

        print('output: ', len(data))
        print('ugas_selected: ', ugas_selected)
        print('spe_selected: ', spe_selected)
        print('cib_selected: ', cib_selected)
        print('pvm_range: ', pvm_range)
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
        return [build_flip(d) for d in data]

    @dashapp.callback(
        Output("visdcc", "run"),
        Input("tiles-content", "children")
    )
    def run_js(children):
        if children:
            return """
            const arrows = toArray(document.getElementsByTagName('img'));
            arrows.forEach( (arrow) => arrow.addEventListener('click', flipCard))
            """


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

    # MODAL TOGGLE
    @dashapp.callback(
        Output("pds-modal", "is_open"),
        Input("modal-btn", "n_clicks"),
        State("pds-modal", "is_open"),

    )
    def toggle_modal(n, is_open):
        if n :
            return not is_open
        return is_open



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

    """
    # OFFCANVAS TOGGLE
    @dashapp.callback(
        Output("offcanvas", "is_open"),
        Input("open-offcanvas", "n_clicks"),
        [State("offcanvas", "is_open")],
    )
    def toggle_offcanvas(n1, is_open):
        if n1:
            return not is_open
        return is_open
    """
