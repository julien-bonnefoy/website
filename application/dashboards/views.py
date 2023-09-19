# -*- coding: utf-8 -*-
""" OCR VIEWS

BLUEPRINT: dash_bp
ROUTES FUNCTIONS: crossfilter_dash, iris_dash, orange_dash
OTHER FUNCTIONS:
"""
from flask import render_template, Blueprint, redirect, url_for
from .biocodex.models import Identity
from .biocodex.forms import EditForm
from application import db

# Blueprint Configuration
dash_bp = Blueprint(
    'dash_bp',
    __name__,
    static_folder='../static',
    template_folder='../templates',
    url_prefix="/dash"
)


@dash_bp.route('/crossfilter', methods=['GET'])
def crossfilter_dash():
    return render_template(
        'dashboards/dashboard.html',
        dash_url="/dash/crossfilter/",
        title="Crossfilter"
    )


@dash_bp.route('/iris', methods=['GET'])
def iris_dash():
    return render_template(
        'dashboards/dashboard.html',
        dash_url="/dash/iris/",
        titile="Iris"
    )


@dash_bp.route('/biocodex', methods=['GET'])
def biocodex_dash():
    return render_template(
        'dashboards/dashboard.html',
        dash_url="/dash/biocodex/",
        title="Biocodex"
    )
