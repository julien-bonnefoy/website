from application import create_flask_server
from application.dash import dash_apps_factory
from application import cli
from application import db
from application.users.models import User
from application.dash.biocodex.models import Identity, Adress, Cdb, Connection
from flask import g, session

server = create_flask_server()
app = dash_apps_factory(server)
cli.register(app)
app.app_context().push()

@app.before_request
def fix_missing_csrf_token():
    app.config['WTF_CSRF_TIME_LIMIT'] = 7200
    if app.config['WTF_CSRF_FIELD_NAME'] not in session:
        if app.config['WTF_CSRF_FIELD_NAME'] in g:
            g.pop(app.config['WTF_CSRF_FIELD_NAME'])
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
        'Connections': Connection
    }

if __name__ == "main":
    app.run_server()