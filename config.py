import os

basedir = os.path.abspath(os.path.dirname(__file__))
"""
Configuration data for the flask server. Currently only used for retrieval of db urls
"""

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
