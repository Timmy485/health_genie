import os
from os import environ
from dotenv import load_dotenv
load_dotenv()


class Config:
    """Base config."""
    SECRET_KEY = environ.get('SECRET_KEY') or \
        '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
    FLASK_SECRET = SECRET_KEY
    SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME')


class ProdConfig(Config):
    FLASK_ENV = environ.get('FLASK_ENV')
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    FLASK_ENV = environ.get('FLASK_ENV')
    DEBUG = True
    TESTING = True

class TestConfig(Config):
    FLASK_ENV = environ.get('FLASK_ENV')
    DEBUG = True
    TESTING = True


CONFIGS = {
    "development": DevConfig,
    "production": ProdConfig,
    "test": TestConfig,
    "default": DevConfig
}
