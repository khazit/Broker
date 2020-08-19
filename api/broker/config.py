import os


class Config:
    pass

class ProdConfig(Config):
    FLASK_ENV = "production"
    TESTING = False
    DEBUG = False
    DATABASE_URI = ""

class DevConfig(Config):
    FLASK_ENV = "development"
    TESTING = False
    DEBUG = True
    DATABASE_URI = "data.db"

class TestConfig(Config):
    FLASK_ENV = "testing"
    TESTING = True
    DEBUG = True
    DATABASE_URI = "tests/test_data/data.db"
