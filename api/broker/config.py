"""Config classes."""

# pylint: disable=R0903


class Config:
    """Config base class"""


class ProdConfig(Config):
    """Production configuration"""
    FLASK_ENV = "production"
    TESTING = False
    DEBUG = False
    DATABASE_URI = ""


class DevConfig(Config):
    """Development configuration"""
    FLASK_ENV = "development"
    TESTING = False
    DEBUG = True
    DATABASE_URI = "/data/data.db"
    STORAGE_URI = "/data"


class TestConfig(Config):
    """Testing configuration"""
    FLASK_ENV = "testing"
    TESTING = True
    DEBUG = True
    DATABASE_URI = "tests/test_data/data.db"
    STORAGE_URI = "tests/test_data/data"
