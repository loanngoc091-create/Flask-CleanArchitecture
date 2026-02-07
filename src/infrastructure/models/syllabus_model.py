# infrastructure/models/syllabus_model.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, text
from infrastructure.databases.base import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import func
from infrastructure.databases.db import db

class SyllabusModel(Base):
    __tablename__ = "syllabi"

    syllabus_id = Column(Integer, primary_key=True)
    version_number = Column(Integer)
    status = Column(String(50))
    create_date = Column(DateTime,
    default=func.now())
    file_path = db.Column(db.String(255))

    course_id = Column(Integer, ForeignKey("courses.course_id"))
    lecturer_id = Column(Integer, ForeignKey("users.user_id"))
    course = relationship("Course", back_populates="syllabi")
    clos = relationship("CLO", back_populates="syllabus")
    approvals = relationship("Approval", back_populates="syllabus")


