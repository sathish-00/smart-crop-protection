# smart-crop-protection/backend/config.py
import os
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class Config(object):
    DEBUG = False
    SECRET_KEY = 'your-secret-key-replace-me'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'backend', 'dev.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False 

class DevelopmentConfig(Config):
    DEBUG = True