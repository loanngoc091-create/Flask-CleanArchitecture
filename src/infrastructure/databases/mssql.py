# infrastructure/databases/mssql.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config
from infrastructure.databases.base import Base
import infrastructure.models  # ⚠️ BẮT BUỘC import model

engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URI,
    echo=True
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

def get_session():
    return SessionLocal()

def init_mssql():
    Base.metadata.create_all(bind=engine)
