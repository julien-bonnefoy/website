from flask import Blueprint, render_template

# Blueprint Configuration
clock_bp = Blueprint(
    'clock_bp',
    __name__,
    template_folder='../templates/',
    static_folder='../static/',
    url_prefix='/clock'
)


@clock_bp.route('/clock/', methods=['GET'])
def clock():
    return render_template(
        'clock/clock.html',
        title='Clock Clock 24',
    )