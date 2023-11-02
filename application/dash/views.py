# -*- coding: utf-8 -*-
from flask import render_template, Blueprint

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


@dash_bp.route('/biocodex', methods=['GET', 'POST'])
def biocodex():
    return render_template(
        'dashboards/dashboard.html',
        dash_url="/dash/biocodex/",
        title="Biocodex"
    )

