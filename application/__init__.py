# -*- coding: utf-8 -*-
from application import cli, commands
from application.dash import dash_apps_factory
import logging
import sys
from flask import Flask, render_template
from application.extensions import bcrypt, cache, db, flask_static_digest, lm, debug_toolbar
from application.extensions import migrate, mail, moment, bootstrap, csrf_protect
from application.users.models import User
from elasticsearch import Elasticsearch
from application.dash.biocodex.models import Identity, Adress, Cdb, Connection

from application.config import config, basedir

def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    csrf_protect._exempt_views.add('dash.dash.dispatch')
    lm.init_app(app)
    # debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    flask_static_digest.init_app(app)
    mail.init_app((app))
    moment.init_app(app)



    return None


def register_blueprints(server):
    """Register Flask blueprints."""
    from application.home.views import home_bp
    from application.auth.views import auth_bp
    from application.dash.views import dash_bp
    from application.ocr.views import ocr_bp
    from application.users.views import user_bp
    from application.clock.views import clock_bp

    server.register_blueprint(home_bp)
    server.register_blueprint(auth_bp)
    server.register_blueprint(dash_bp)
    server.register_blueprint(ocr_bp)
    server.register_blueprint(user_bp)
    server.register_blueprint(clock_bp)


    return None


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribut
        # e; default to 500
        error_code = getattr(error, "code", 500)
        return render_template(f"errors/{error_code}.html"), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)

    return None


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {'db': db, 'User': User}

    app.shell_context_processor(shell_context)

    return None


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)

    return None


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)

    return None


def create_flask_server():

    server = Flask(__name__)
    server.app_context().push()
    server.config.from_object(config.get('prod'))
    csrf_protect._exempt_views.add('dash.dash.dispatch')
    bootstrap.init_app(server)
    register_extensions(server)
    register_blueprints(server)
    register_errorhandlers(server)
    register_shellcontext(server)
    register_commands(server)
    configure_logger(server)
    server.elasticsearch = Elasticsearch([server.config['ELASTICSEARCH_URL']]) if server.config['ELASTICSEARCH_URL'] else None

    return server
