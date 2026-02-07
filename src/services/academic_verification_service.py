from domain.models.approval import Approval
from infrastructure.models.user_model import User as UserModel

class AcademicVerificationService:

    def __init__(self, uow):
        self.uow = uow

    def verify_syllabus(self, command, user_id):

        with self.uow:

            user = self.uow.users.get_by_id(user_id)
            if not user:
                raise Exception("User not found")

            if user.role_code != "ACADEMIC_AFFAIRS":
                raise Exception("You are not Academic Affairs")

            syllabus = self.uow.syllabuses.get_by_id(command.syllabus_id)
            if not syllabus:
                raise Exception("Syllabus not found")

            if syllabus.status != "HodApproved":
                raise Exception("Syllabus not waiting for Academic verification")

            # ✅ UPDATE DB QUA ORM
            decision = command.decision.upper()
            self.uow.syllabuses.update_status(
                command.syllabus_id,
                "AcademicApproved" if command.decision == "Approved" else "Rejected"
            )

            # 🔥 LẤY role_id TỪ ORM
            user_orm = (
                self.uow.session
                .query(UserModel)
                .filter(UserModel.user_id == user.user_id)
                .first()
            )

            role_id = user_orm.roles[0].role.role_id

            approval = Approval(
                syllabus_id=command.syllabus_id,
                status=command.decision,
                step=2,
                role_id=role_id,
                user_id=user.user_id,
                
            )

            self.uow.approvals.add(approval)
