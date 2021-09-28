from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config_parser import user, passwd, db_name, host

engine = create_engine(f"mariadb+pymysql://{user}:{passwd}@{host}/{db_name}?charset=utf8mb4")

Base = declarative_base()