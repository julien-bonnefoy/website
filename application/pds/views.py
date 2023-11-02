# -*- coding: utf-8 -*-
""" PDS VIEWS
BLUEPRINT: pds_bp
ROUTES FUNCTIONS:
OTHER FUNCTIONS:
"""
from flask import render_template, Blueprint, request, flash, redirect, url_for
from application.pds.forms import IdentityForm, CdbForm
from application.dash.biocodex.functions import doctor_colors

# Blueprint Configuration
pds_bp = Blueprint(
    'pds_bp',
    __name__,
    static_folder='./static',
    template_folder='./templates',
    # url_prefix="/dash"
)

from .controllers import list_all_pds_ctrlr, create_pds_ctrlr, retrieve_pds_ctrlr, update_pds_ctrlr


@pds_bp.route("/pds", methods=['GET', 'POST'])
def list_or_create_pds():

    if request.method == 'GET':
        return list_all_pds_ctrlr()

    if request.method == 'POST':
        return create_pds_ctrlr()

    else:
        return 'Method is Not Allowed'


@pds_bp.route("/dash/biocodex/pds/<pds_id>", methods=['GET', 'POST'])
def show_or_update_pds(pds_id):

    if request.method == 'GET':

        return render_template("partials/modal-frame.html", src=f"/dash/biocodex/pds/{pds_id}")

    elif request.method == 'POST':
        return update_pds_ctrlr(pds_id)

    else:
        return 'Method is Not Allowed'
