from datetime import datetime

class ApprovalHistory:

    def __init__(self, syllabus_id, status, approver_role, comment=None):
        self.syllabus_id = syllabus_id
        self.status = status
        self.approver_role = approver_role
        self.comment = comment
        self.created_at = datetime.utcnow()
