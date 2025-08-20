class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'your_secret_key_here'
    DATABASE_URI = 'sqlite:///your_database.db'
    JSON_SORT_KEYS = False

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URI = 'sqlite:///dev_database.db'

class TestingConfig(Config):
    TESTING = True
    DATABASE_URI = 'sqlite:///test_database.db'

class ProductionConfig(Config):
    DATABASE_URI = 'sqlite:///prod_database.db'