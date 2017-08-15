# Default config
class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = 'p@ssword'
    USER_TABLE_NAME = 'registered_user'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost:5432'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class CloudConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False

