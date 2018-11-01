# /instance/config.py

import os


class Config(object):
    """
        Parent configuration class.
    """
    DEBUG = False
    DATABASE_URL = os.getenv('DATABASE_URL')


class DevelopmentConfig(Config):
    """
        Configurations for Development.
    """
    DEBUG = True


class TestingConfig(Config):
    """
        Configurations for Testing
    """
    TESTING = True
    DEBUG = True
    DATABASE_URL = os.getenv('DATABASE_TEST')

class StagingConfig(Config):
    """
        Configurations for Staging.
    """
    DEBUG = True


class ProductionConfig(Config):
    """
        Configurations for Production.
    """
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}