from sqlalchemy import Column, Integer, String
from infrastructure.databases.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text

class CLO(Base):
    __tablename__ = "clos"

    clo_id = Column(Integer, primary_key=True)
    clo_code = Column(String(50))
    description = Column(Text)

    syllabus_id = Column(Integer, ForeignKey("syllabi.syllabus_id"))

    syllabus = relationship("Syllabus", back_populates="clos")
