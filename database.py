import yaml

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

with open('properties.yml') as f:
    PROPERTIES = yaml.load(f, Loader=yaml.FullLoader)

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{PROPERTIES['USER']}:{PROPERTIES['PASSWORD']}@{PROPERTIES['HOST']}:{PROPERTIES['PORT']}/{PROPERTIES['DATABASE']}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 

# 이 클래스(Base)를 상속하여 ORM 모델 또는 클래스를 생성 
Base = declarative_base()
