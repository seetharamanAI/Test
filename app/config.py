import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev")
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
