# -*- coding: utf-8 -*-
from flask_app import create_app
from config import ProdConfig, DevConfig
from flask_app.dash.orange.models import User
from flask_app.extensions import db

prod = ProdConfig()
dev = DevConfig()
app = create_app(dev)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}