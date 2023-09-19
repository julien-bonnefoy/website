from flask import Blueprint, render_template
from flask_login import login_required
from application.dashboards. biocodex.functions import join_id_adr_cdb

# Blueprint Configuration
pds_bp = Blueprint(
    'pds_bp',
    __name__,
    template_folder='../templates/',
    static_folder='../static/'
)


@pds_bp.route('/pds', methods=['GET'])
@login_required
def display_tiles():
    id_adr = join_id_adr_cdb()
    print(id_adr.columns)
    ciblage = id_adr[id_adr["ciblage"] != 0].copy()
    return render_template("pds/pds.html", id_adr=ciblage)