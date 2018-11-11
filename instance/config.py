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
    os.environ['ENV'] = 'development'
    DATABASE_URL = "dbname='storemanager' host='localhost' port='5432' user='postgres' password='nic'"
    # os.environ["ENV"] ="development"

class TestingConfig(Config):
    """
        Configurations for Testing
    """
    TESTING = True
    DEBUG = True
    # os.environ['ENV'] = 'testing'
    DATABASE_URL = "dbname='storemanager_testdb' host='localhost' port='5432' user='postgres' password='nic'"
   
app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
}