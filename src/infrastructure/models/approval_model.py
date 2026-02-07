# infrastructure/models/approval_model.py
from sqlalchemy import Column, Integer, String, ForeignKey
from infrastructure.databases.base import Base
from sqlalchemy.orm import relationship


class Approval(Base):
    __tablename__ = "approvals"

    approval_id = Column(Integer, primary_key=True)
    status = Column(String(50))
    step = Column(Integer)

    role_id = Column(Integer, ForeignKey("roles.role_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    syllabus_id = Column(Integer, ForeignKey("syllabi.syllabus_id"))

    user = relationship("User", back_populates="approvals")
    syllabus = relationship("SyllabusModel", back_populates="approvals")

