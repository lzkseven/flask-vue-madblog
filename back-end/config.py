import os
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


from setting import MYSQL_PASSWD, MYSQL_USER, MYSQL_HOST, MYSQL_POST, MYSQL_DB

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))




class Config(object):
    #SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL') or \
    #                         'sqlite:///'+os.path.join(basedir,'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_DATABASE_URI = "mysql://%s:%s@%s:%s/%s?charset=utf8" % (MYSQL_USER, MYSQL_PASSWD, MYSQL_HOST, MYSQL_POST, MYSQL_DB)
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'app.db')