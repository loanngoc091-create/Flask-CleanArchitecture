# infrastructure/models/course_model.py
from sqlalchemy import Column, Integer, String, ForeignKey
from infrastructure.databases.base import Base
from sqlalchemy.orm import relationship


class Course(Base):
    __tablename__ = "courses"

    course_id = Column(Integer, primary_key=True)
    course_code = Column(String(50))
    course_name = Column(String(150))
    credits = Column(Integer)

    program_id = Column(Integer, ForeignKey("programs.program_id"))
    lecturer_id = Column(Integer, ForeignKey("users.user_id")) 

    program = relationship("Program", back_populates="courses")
    syllabi = relationship("SyllabusModel", back_populates="course")
