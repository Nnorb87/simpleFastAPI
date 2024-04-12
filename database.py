from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dbauth import dbpass, dbipandport

URL_DATABASE = f'mysql+pymysql://root:{dbpass}@{dbipandport}/fastapi_db_2'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()