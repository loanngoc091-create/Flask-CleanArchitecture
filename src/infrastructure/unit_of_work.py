from infrastructure.databases.db import db
from infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from infrastructure.repositories.syllabus_repository import SyllabusRepository
from infrastructure.repositories.approval_repository import ApprovalRepository

class UnitOfWork:

    def __init__(self):
        self.session = None
        self.users = None
        
    def commit(self):
        self.session.commit()

    def __enter__(self):
        self.session = db.session
        self.users = UserRepositoryImpl(self.session)
        self.syllabuses = SyllabusRepository(self.session)
        self.approvals = ApprovalRepository(self.session)
        
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.session.rollback()
        else:
            self.session.commit()

        
