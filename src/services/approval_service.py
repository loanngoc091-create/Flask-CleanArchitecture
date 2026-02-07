from domain.models.approval import Approval
from infrastructure.models.user_model import User as UserModel


class ApprovalService:

    def __init__(self, uow):
        self.uow = uow

    # ================== HOD APPROVE ==================
    def hod_approve(self, syllabus_id, decision, user_id):

        with self.uow:

            user = self.uow.users.get_by_id(user_id)
            if not user:
                raise Exception("User not found")

            if user.role_code != "HOD":
                raise Exception("You are not HOD")

            syllabus = self.uow.syllabuses.get_by_id(syllabus_id)
            if not syllabus:
                raise Exception("Syllabus not found")

            if syllabus.status != "PendingReview":
                raise Exception("Syllabus not waiting for HOD approval")

            self.uow.syllabuses.update_status(
                syllabus_id,
                "HodApproved" if decision == "APPROVED" else "Rejected"
            )

            role_id = self._get_role_id(user.user_id)

            approval = Approval(
                syllabus_id=syllabus_id,
                status=decision,
                step=1,
                role_id=role_id,
                user_id=user.user_id
            )

            self.uow.approvals.add(approval)

    # ================== PRINCIPAL APPROVE ==================
    def final_approval(self, syllabus_id, decision, user_id):

        with self.uow:

            user = self.uow.users.get_by_id(user_id)
            if not user:
                raise Exception("User not found")

            if user.role_code != "PRINCIPAL":
                raise Exception("You are not Principal")

            syllabus = self.uow.syllabuses.get_by_id(syllabus_id)
            if not syllabus:
                raise Exception("Syllabus not found")

            if syllabus.status != "AcademicApproved":
                raise Exception("Syllabus not waiting for Principal approval")

            self.uow.syllabuses.update_status(
                syllabus_id,
                "Approved" if decision == "APPROVED" else "Rejected"
            )

            role_id = self._get_role_id(user.user_id)

            approval = Approval(
                syllabus_id=syllabus_id,
                status=decision,
                step=3,
                role_id=role_id,
                user_id=user.user_id
            )

            self.uow.approvals.add(approval)

    # ================== PRIVATE HELPER ==================
    def _get_role_id(self, user_id):
        user_orm = (
            self.uow.session
            .query(UserModel)
            .filter(UserModel.user_id == user_id)
            .first()
        )

        if not user_orm or not user_orm.roles:
            raise Exception("User role not found")

        return user_orm.roles[0].role.role_id
