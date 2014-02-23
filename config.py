import os
import sys


class Environments(object):
    Production = 'prod'
    Development = 'dev'
    Testing = 'test'
    Default = Development


def get_env():
    # NOTE(michael): Check if this function is being called by nose.
    for arg in sys.argv:
        if 'nose' in arg:
            return Environments.Testing

    return os.environ.get('FLASK_ENV', Environments.Default)


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE = ':memory:'



class ProductionConfig(Config):
    DATABASE = 'prod.sqlite'


class DevelopmentConfig(Config):
    DATABASE = 'dev.sqlite'
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DATABASE = 'test.sqlite'


def config():
    env = get_env()
    if env == Environments.Development:
        return 'config.DevelopmentConfig'
    elif env == Environments.Production:
        return 'config.ProductionConfig'
    elif env == Environments.Testing:
        return 'config.TestingConfig'
    return 'config.Config'


def get_config(key):
    env = get_env()
    config = Config
    if env == Environments.Development:
        config = DevelopmentConfig
    elif env == Environments.Production:
        config = ProductionConfig
    elif env == Environments.Testing:
        config = TestingConfig

    return getattr(config, key)


def is_production():
    return get_env() == Environments.Production


def is_dev():
    return get_env() == Environments.Development

def is_test():
    return get_env() == Environments.Testing
