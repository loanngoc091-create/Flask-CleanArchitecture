from infrastructure.models.verification_model import VerificationModel

class VerificationRepository:

    def __init__(self, session):
        self.session = session

    def add(self, verification):
        orm = VerificationModel(
            syllabus_id=verification.syllabus_id,
            status=verification.status,
            comment=verification.comment,
            role_id=verification.role_id,
            user_id=verification.user_id,
            created_at=verification.created_at
        )
        self.session.add(orm)
