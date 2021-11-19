# -*- coding: utf-8 -*-
""" OCR VIEWS

BLUEPRINT: dash_bp
ROUTES FUNCTIONS: crossfilter_dash, iris_dash, orange_dash
OTHER FUNCTIONS:
"""
from flask import render_template, Blueprint

# Blueprint Configuration
dash_bp = Blueprint(
    'dash_bp',
    __name__,
    static_folder='../static',
    template_folder='./templates',
    url_prefix="/dash"
)


@dash_bp.route('/crossfilter', methods=['GET'])
def crossfilter_dash():
    return render_template(
        'partials/iframe.html',
        dash_url="/dash/crossfilter"
    )


@dash_bp.route('/iris', methods=['GET'])
def iris_dash():
    return render_template(
        'partials/iframe.html',
        dash_url="/dash/iris"
    )


@dash_bp.route('/orange', methods=['GET'])
def orange_dash():
    return render_template(
        'partials/no_iframe.html',
        dash_url="/dash/orange"
    )

