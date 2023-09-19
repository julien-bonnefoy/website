from app import create_flask_server, dash_apps_factory, cli
from app.extensions import db
from app.users.models import User


server = create_flask_server()
app = dash_apps_factory(server)
server=app.server
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User
    }
