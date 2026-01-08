# infrastructure/models/program_model.py
from sqlalchemy import Column, Integer, String
from infrastructure.databases.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

class Program(Base):
    __tablename__ = "programs"

    program_id = Column(Integer, primary_key=True)
    year_applied = Column(Integer)
    program_name = Column(String(150))

    department_id = Column(Integer, ForeignKey("departments.department_id"))

    department = relationship("Department", back_populates="programs")
    courses = relationship("Course", back_populates="program")
    plos = relationship("PLO", back_populates="program")
