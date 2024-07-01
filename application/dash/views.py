# -*- coding: utf-8 -*-
from flask import render_template, Blueprint, request
from application.dash.controllers import list_all_pds_ctrlr, create_pds_ctrlr, update_pharma_ctrlr, update_pds_ctrlr

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


@dash_bp.route('/dash/biocodex/<page>', methods=['GET', 'POST'])
def biocodex(page):
    if page is None:
        tpl = render_template(
            'dashboards/dashboard.html',
            dash_url=f"/dash/biocodex/",
            title="Biocodex"
        )
    else:
        tpl = render_template(
            'dashboards/dashboard.html',
            dash_url=f"/dash/biocodex/{page}/",
            title=page.title()
        )
    return tpl


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

    url = request.environ['HTTP_REFERER']
    form = request.form
    if request.method == 'POST':

        return update_pds_ctrlr(pds_id, form, url)


@dash_bp.route("/dash/biocodex/pharma/<pha_id>", methods=['POST'])
def show_or_update_pharma(pha_id):


    url = request.environ['HTTP_REFERER']
    form = request.form
    print(form['ddv'], type(form['ddv']))
    if request.method == 'POST':

        return update_pharma_ctrlr(pha_id, form, url)
