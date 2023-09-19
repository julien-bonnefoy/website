from application import create_flask_server, dash_apps_factory, cli
from application.extensions import db
from application.users.models import User


server = create_flask_server()
app = dash_apps_factory(server)
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User
    }
