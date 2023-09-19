from os import environ, path



class Config(object):
    """Base config."""

    SECRET_KEY = ("93807f0a7b2e5577c4e3b4f93e70ad4de7ecc9c6d0262652d3a47be8700379e0")

    CACHE_TYPE = "simple"

    SQLALCHEMY_DATABASE_URI = "sqlite:///application/data/biocodex.db"
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

    ELASTICSEARCH_URL = environ.get('ELASTICSEARCH_URL')


class ProdConfig(Config):
    pass


class DevConfig(Config):

    SESSION_COOKIE_SECURE = False
    DEBUG = True


class TestConfig(Config):
    TESTING = True
    SESSION_COOKIE_SECURE = False
    DEBUG = True
