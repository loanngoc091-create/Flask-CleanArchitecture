# infrastructure/models/user_model.py
from sqlalchemy import Column, Integer, String
from infrastructure.databases.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

class Department(Base):
    __tablename__ = "departments"

    department_id = Column(Integer, primary_key=True)
    department_code = Column(String(50))
    department_name = Column(String(150))

    programs = relationship("Program", back_populates="department")
