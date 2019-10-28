import os

postgres_url = os.environ['DATABASE_URL']
test_postgres_url = os.environ['TEST_DATABASE_URL']
dev_postgres_url = os.environ['DEV_DATABASE_URL']

basedir = os.path.abspath(os.path.dirname(__file__))


class DevelopmentConfig():
    DEBUG = True
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = dev_postgres_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig():
    DEBUG = True
    TESTING = True
    ENV = 'testing'
    SQLALCHEMY_DATABASE_URI = test_postgres_url
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig():
    DEBUG = False
    ENV = 'production'
    SQLALCHEMY_DATABASE_URI = postgres_url


config_by_name = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig
)
