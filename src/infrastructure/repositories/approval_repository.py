from infrastructure.models.approval_model import Approval

class ApprovalRepository:

    def __init__(self, session):
        self.session = session

    def add(self, approval):
        orm = Approval(
            syllabus_id=approval.syllabus_id,
            status=approval.status,
            step=approval.step,
            role_id=approval.role_id,
            user_id=approval.user_id
        )
        self.session.add(orm)
