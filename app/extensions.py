# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the flask_app factory located in flask_app.py."""
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_static_digest import FlaskStaticDigest
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l
from flask_bootstrap import Bootstrap


db = SQLAlchemy()
bcrypt = Bcrypt()
csrf_protect = CSRFProtect()
lm = LoginManager()
lm.login_view = 'auth_bp.login'
lm.login_message = _l('You need to log in to access this page.')

migrate = Migrate()
cache = Cache()
debug_toolbar = DebugToolbarExtension()
flask_static_digest = FlaskStaticDigest()
mail = Mail()
moment = Moment()
babel = Babel()
bootstrap = Bootstrap()