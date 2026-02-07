from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from infrastructure.databases.base import Base

class Verification(Base):
    __tablename__ = "verifications"

    verification_id = Column(Integer, primary_key=True)
    decision = Column(String(50))
    comment = Column(String(255))
    verify_date = Column(DateTime, default=datetime.utcnow)

    syllabus_id = Column(Integer, ForeignKey("syllabi.syllabus_id"))
