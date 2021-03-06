# -*- coding: utf-8 -*-
import logging
import sys
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from . import commands, users
from flask_app.extensions import bcrypt, cache, csrf_protect, db, flask_static_digest, login_manager #, debug_toolbar
from flask_app.extensions import migrate, mail, moment, babel
from flask_app.dash import dash_apps_facrory
from flask_app.users.models import User
from flask_moment import Moment

bootstrap = Bootstrap()


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    csrf_protect._exempt_views.add('dash.dash.dispatch')
    login_manager.init_app(app)
    # debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    flask_static_digest.init_app(app)
    mail.init_app((app))
    moment.init_app(app)
    babel.init_app(app)
    return None


def register_blueprints(server):
    """Register Flask blueprints."""
    from flask_app.home.views import home_bp
    from flask_app.clock.views import clock_bp
    from flask_app.dash.views import dash_bp
    from flask_app.ocr.views import ocr_bp
    from .users.views import user_bp
    server.register_blueprint(clock_bp)
    server.register_blueprint(dash_bp)
    server.register_blueprint(ocr_bp)
    server.register_blueprint(home_bp)
    server.register_blueprint(user_bp)

    return None


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
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
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.
    :param config_object: The configuration object to use.
    """
    server = Flask(__name__)

    if server.config["ENV"] == "production":
        server.config.from_object("config.ProdConfig")
    else:
        server.config.from_object("config.DevConfig")

    bootstrap.init_app(server)
    register_extensions(server)
    register_blueprints(server)
    register_errorhandlers(server)
    register_shellcontext(server)
    register_commands(server)
    configure_logger(server)

    return server

