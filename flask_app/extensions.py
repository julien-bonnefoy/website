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


bcrypt = Bcrypt()
csrf_protect = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = 'home_bp.index'
login_manager.login_message = _l('Please log in to access this page.')
db = SQLAlchemy()
migrate = Migrate()
cache = Cache()
# debug_toolbar = DebugToolbarExtension()
flask_static_digest = FlaskStaticDigest()
mail = Mail()
moment = Moment()
babel = Babel()
