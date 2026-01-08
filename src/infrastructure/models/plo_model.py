# infrastructure/models/user_model.py
from sqlalchemy import Column, Integer, String
from infrastructure.databases.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text

class PLO(Base):
    __tablename__ = "plos"

    plo_id = Column(Integer, primary_key=True)
    plo_code = Column(String(50))
    description = Column(Text)

    program_id = Column(Integer, ForeignKey("programs.program_id"))

    program = relationship("Program", back_populates="plos")
