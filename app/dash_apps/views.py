from flask import render_template, Blueprint

# Blueprint Configuration
dash_bp = Blueprint(
    'dash_bp',
    __name__,
    static_folder='../static',
    template_folder='./templates',
    url_prefix="/dash_apps"
)


@dash_bp.route('/crossfilter', methods=['GET'])
def crossfilter_dash():
    return render_template(
        'iframe.html',
        dash_url="/dash_apps/crossfilter/"
    )


@dash_bp.route('/iris', methods=['GET'])
def iris_dash():
    return render_template(
        'iframe.html',
        dash_url="/dash_apps/iris/"
    )


@dash_bp.route('/orange', methods=['GET'])
def orange_dash():
    return render_template(
        'no_iframe.html',
        dash_url="/dash_apps/orange/"
    )

