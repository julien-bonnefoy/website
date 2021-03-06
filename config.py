from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

driver = environ.get("DRIVER")
server = environ.get("SERVER")
database = environ.get("DATABASE")
username = environ.get("USERNAME")
password = environ.get("PASSWORD")
port = environ.get("PORT")

CONN_STR = f'DRIVER={driver};PORT=1433;SERVER={server};DATABASE={database};UID={username};PWD={password}'

class Config(object):
    """Base config."""

    SECRET_KEY = environ.get('SECRET_KEY')

    CACHE_TYPE = "simple"

    LANGUAGES = ['en', 'fr']

    STATIC_FOLDER = environ.get('STATIC_FOLDER')
    TEMPLATES_FOLDER = environ.get('TEMPLATES_FOLDER')

    SQLALCHEMY_DATABASE_URI = environ.get('PROD_DATABASE_URL') + CONN_STR
    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')

    MAIL_SERVER = environ.get('MAIL_SERVER')
    MAIL_PORT = int(environ.get('MAIL_PORT') or 25)
    MAIL_USE_SSL = environ.get('MAIL_USE_SSL') is not None
    MAIL_USE_TLS = environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = environ.get('MAIL_DEFAULT_SENDER')
    ADMINS = environ.get('ADMINS')

    MS_TRANSLATOR_KEY = environ.get('MS_TRANSLATOR_KEY')
    LOG_TO_STDOUT = environ.get('LOG_TO_STDOUT')
    ELASTICSEARCH_URL = environ.get('ELASTICSEARCH_URL')
    REDIS_URL = environ.get('REDIS_URL') or 'redis://'
    TEMPLATES_AUTO_RELOAD = environ.get('TEMPLATES_AUTO_RELOAD')
    RECAPTCHA_PUBLIC_KEY = environ.get('RC_SITE_KEY')
    RECAPTCHA_PRIVATE_KEY = environ.get('RC_SECRET_KEY')
    DEBUG_TB_INTERCEPT_REDIRECTS = environ.get('DEBUG_TB_INTERCEPT_REDIRECTS')

    SESSION_COOKIE_SECURE = True


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = environ.get('DEV_DATABASE_URL')
    SESSION_COOKIE_SECURE = False


class  TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = environ.get('DEV_DATABASE_URL')
    SESSION_COOKIE_SECURE = False