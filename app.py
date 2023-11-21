from application import create_flask_server
from application.dash import dash_apps_factory
from application import cli
from application import db
from application.users.models import User
from application.dash.biocodex.models import Identity, Adress, Cdb, Connections


server = create_flask_server()
app = dash_apps_factory(server)
cli.register(app)
app.app_context().push()
"""
server = Server(app.wsgi_app)
# server.watch
server.serve()
"""

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Identity': Identity,
        'Adress': Adress,
        'Cdb': Cdb,
        'Connections': Connections
    }
