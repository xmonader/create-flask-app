import os

PRODUCTION = False
DBDIR = os.path.join(os.getcwd(), "db")
DBPATHDEV = os.path.join(os.getcwd(), "db", "development.db")
DBPATHPROD = os.path.join(os.getcwd(), "db", "production.db")
DBPATH = DBPATHDEV
BACKEND = "sqlite3"

if PRODUCTION is True:
    DBPATH = DBPATHPROD

SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(DBPATH)
SQLALCHEMY_ECHO = False
SQLALCHEMY_RECORD_QUERIES = True

SECRET_KEY = "av3rys3ckretk3y!@#{}!;;"
