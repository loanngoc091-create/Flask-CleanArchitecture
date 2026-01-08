# infrastructure/models/syllabus_model.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from infrastructure.databases.base import Base
from datetime import datetime
from sqlalchemy.orm import relationship


class Syllabus(Base):
    __tablename__ = "syllabi"

    syllabus_id = Column(Integer, primary_key=True)
    version_number = Column(Integer)
    status = Column(String(50))
    create_date = Column(Date)

    course_id = Column(Integer, ForeignKey("courses.course_id"))

    course = relationship("Course", back_populates="syllabi")
    clos = relationship("CLO", back_populates="syllabus")
    approvals = relationship("Approval", back_populates="syllabus")


