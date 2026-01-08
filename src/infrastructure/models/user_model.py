# infrastructure/models/user_model.py
from sqlalchemy import Column, Integer, String
from infrastructure.databases.base import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    full_name = Column(String(150))
    status = Column(String(150))
    email = Column(String(150))

    roles = relationship("UserRole", back_populates="user")
    approvals = relationship("Approval", back_populates="user")

