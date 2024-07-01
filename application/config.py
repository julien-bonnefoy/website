from dotenv import load_dotenv
import os

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

host = os.environ.get("HOST")
database = os.environ.get("DATABASE")
user = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")
port = os.environ.get("PORT")



def read_credentials():
    """
    Return user’s credentials from the environment variables file and
    raise a an exception if the credentials are not present

    Raises:
        NotImplementedError: [description]
    """
    load_dotenv()

    USER_EMAIL = os.getenv("USER_EMAIL")
    USER_PASSWORD = os.getenv("USER_PASSWORD")
    if USER_EMAIL and USER_PASSWORD:
        return USER_EMAIL, USER_PASSWORD
    else:
        raise ValueError('Please add a .env file and write the credentials in it, refer to the sample')


class Config(object):
    """Base config."""

    SECRET_KEY = os.environ.get('SECRET_KEY')

    LANGUAGES = ['en', 'fr']

    STATIC_FOLDER = os.environ.get('STATIC_FOLDER')
    TEMPLATES_FOLDER = os.environ.get('TEMPLATES_FOLDER')

    FLASK_DEBUG = True

    SQLALCHEMY_DATABASE_URI = f'postgresql://{os.environ.get("USERNAME")}:{os.environ.get("PASSWORD")}@{os.environ.get("HOST")}:{os.environ.get("PORT")}/{os.environ.get("DATABASE")}'  # or other relevant config var
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL') is not None
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    ADMINS = os.environ.get('ADMINS')

    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'
    TEMPLATES_AUTO_RELOAD = os.environ.get('TEMPLATES_AUTO_RELOAD')
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RC_SITE_KEY')
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RC_SECRET_KEY')
    DEBUG_TB_INTERCEPT_REDIRECTS = os.environ.get('DEBUG_TB_INTERCEPT_REDIRECTS')

    SESSION_COOKIE_SECURE = True


class ProdConfig(Config):
    pass


class DevConfig(Config):

    SESSION_COOKIE_SECURE = False
    DEBUG = True
    WTF_CSRF_ENABLED = False


class TestConfig(Config):
    TESTING = True
    SESSION_COOKIE_SECURE = False
    DEBUG = True


config = {
    'dev': DevConfig(),
    'prod': ProdConfig(),
    'default': DevConfig(),
}

