from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote  
from .config import settings



sql_alchemy_db_url= f'postgresql://{settings.database_username}:%s@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'% quote(settings.database_password)

engine= create_engine(sql_alchemy_db_url)
#engine = create_engine('postgresql://postgres:%s@localhost/FastApi demobase' % quote('so@longastic'))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base= declarative_base()

