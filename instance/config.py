import os

class Config(object):
    """
        Parent configuration class.
    """
    DEBUG = False
    DATABASE_URL = os.getenv('DATABASE_URL')
    print(DATABASE_URL)


class DevelopmentConfig(Config):
    """
        Configurations for Development.
    """
    DEBUG = True
    DATABASE_URL = "dbname='storemanager_testdb' host='localhost' port='5432' user='postgres' password='nic'"


class TestingConfig(Config):
    """
        Configurations for Testing
    """
    TESTING = True
    DEBUG = True
    TESTING_DATABASE_URL = "dbname='storemanager_testdb' host='localhost' port='5432' user='postgres' password='nic'"
    # DATABASE_URL = os.getenv('DATABASE_TEST')

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
