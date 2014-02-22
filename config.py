import os


class Environments(object):
    Production = 'prod'
    Development = 'dev'
    Testing = 'test'
    Default = Development


def get_env():
    return os.environ.get('FLASK_ENV') or Environments.Default


class Config(object):
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


def get_config():
    env = get_env()
    if env == Environments.Development:
        return 'config.DevelopmentConfig'
    elif env == Environments.Production:
        return 'config.ProductionConfig'
    elif env == Environments.Testing:
        return 'config.TestingConfig'
    return 'config.Config'


def is_production():
    return get_env() == Environments.Production


def is_dev():
    return get_env() == Environments.Development
