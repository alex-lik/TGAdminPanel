<<<<<<< HEAD
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
=======
from config import SQLALCHEMY_DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

if 'sqlite' in SQLALCHEMY_DATABASE_URL:
    """ Надо только для sqlite """
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    """ Для остальных БД """
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

>>>>>>> abd87a6c29e9f56783cac546c133769c128e472a
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
