# -*- coding: utf-8 -*-
from flask_app.extensions import db
from flask_app.users.models import User
from flask_app.dash import  dash_apps_facrory
from flask_app import create_flask_server, cli


server = create_flask_server()
app = dash_apps_facrory(server)
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User,}

from flask_app.users import forms, models


if __name__ == "main":
    app.run_server()
