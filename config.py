from os import environ, path
from dotenv import load_dotenv
from flask_app.database import connect_to_azure

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config(object):
    """Base config."""
    CACHE_TYPE = "simple"
    FLASK_APP = environ.get("FLASK_APP")
    APP_NAME = environ.get("APP_NAME")
    SECRET_KEY = environ.get('SECRET_KEY')
    STATIC_FOLDER = environ.get('STATIC_FOLDER')
    TEMPLATES_FOLDER = environ.get('TEMPLATES_FOLDER')
    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')
    MAIL_SERVER = environ.get('MAIL_SERVER')
    MAIL_PORT = int(environ.get('MAIL_PORT') or 25)
    MAIL_USE_SSL = environ.get('MAIL_USE_SSL') is not None
    MAIL_USE_TLS = environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = environ.get('MAIL_DEFAULT_SENDER')
    ADMINS = environ.get('ADMINS')
    LANGUAGES = ['en', 'es']
    MS_TRANSLATOR_KEY = environ.get('MS_TRANSLATOR_KEY')
    LOG_TO_STDOUT = environ.get('LOG_TO_STDOUT')
    ELASTICSEARCH_URL = environ.get('ELASTICSEARCH_URL')
    REDIS_URL = environ.get('REDIS_URL') or 'redis://'
    TEMPLATES_AUTO_RELOAD = environ.get('TEMPLATES_AUTO_RELOAD')
    RECAPTCHA_PUBLIC_KEY = environ.get('RC_SITE_KEY')
    RECAPTCHA_PRIVATE_KEY = environ.get('RC_SECRET_KEY')

class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
