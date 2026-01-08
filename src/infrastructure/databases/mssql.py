# infrastructure/databases/mssql.py
from sqlalchemy import create_engine
from config import Config
from infrastructure.databases.base import Base
import infrastructure.models  
from sqlalchemy.orm import sessionmaker

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

def init_mssql():
    Base.metadata.create_all(bind=engine)
