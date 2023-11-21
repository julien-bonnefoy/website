# -*- coding: utf-8 -*-
from flask import render_template, Blueprint, request
from application.dash.controllers import list_all_pds_ctrlr, create_pds_ctrlr, retrieve_pds_ctrlr, update_pds_ctrlr
from application.dash.biocodex.functions import df, build_modal, build_tile_front
from application.dash.biocodex.forms import MegaForm
from dash import html
import dash_leaflet.express as dlx
import io

# Blueprint Configuration
dash_bp = Blueprint(
    'dash_bp',
    __name__,
    static_folder='./static',
    template_folder='./templates'
)




@dash_bp.route('/crossfilter', methods=['GET', 'POST'])
def crossfilter_dash():
    return render_template(
        'dashboards/dashboard.html',
        dash_url="/dash/crossfilter/",
        title="Crossfilter"
    )


@dash_bp.route('/iris', methods=['GET', 'POST'])
def iris_dash():
    return render_template(
        'dashboards/dashboard.html',
        dash_url="/dash/iris/",
        titile="Iris"
    )


@dash_bp.route('/dash/biocodex', methods=['GET', 'POST'])
def biocodex():
    return render_template(
        'dashboards/dashboard.html',
        dash_url="/dash/biocodex/",
        title="Biocodex"
    )


@dash_bp.route("/dash/biocodex/pds", methods=['GET', 'POST'])
def list_or_create_pds():

    if request.method == 'GET':
        return list_all_pds_ctrlr()

    if request.method == 'POST':
        return create_pds_ctrlr()

    else:
        return 'Method is Not Allowed'


@dash_bp.route("/dash/biocodex/pds/<pds_id>", methods=['POST'])
def show_or_update_pds(pds_id):

    form = request.form
    print(request.environ['HTTP_REFERER'])
    url = request.environ['HTTP_REFERER']

    if request.method == 'POST':
        print('posting')
        return update_pds_ctrlr(pds_id, form, url)
