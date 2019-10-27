import os

postgres_url = os.environ['DATABASE_URL']

basedir = os.path.abspath(os.path.dirname(__file__))


class DevelopmentConfig():
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = postgres_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig():
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = postgres_url
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig():
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = postgres_url


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)