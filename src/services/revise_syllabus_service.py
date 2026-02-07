from domain.models.syllabus import Syllabus
from infrastructure.models.syllabus_model import SyllabusModel


class ReviseSyllabusService:

    def __init__(self, uow):
        self.uow = uow

    def get_syllabus_detail(self, syllabus_id):
        orm = self.uow.syllabus_repo.get_by_id(syllabus_id)

        if not orm:
            raise Exception("Syllabus not found")

        return {
            "syllabus_id": orm.syllabus_id,
            "version_number": orm.version_number,
            "status": orm.status,
            "description": getattr(orm, "description", None)
        }

    def update_syllabus_file(self, syllabus_id, file_path, lecturer_id):
        with self.uow:

            user = self.uow.users.get_by_id(lecturer_id)
            if not user or user.role_code != "LECTURER":
                raise Exception("Only lecturer can update syllabus")

            syllabus = self.uow.syllabuses.get_by_id(syllabus_id)
            if not syllabus:
                raise Exception("Syllabus not found")

            if syllabus.status not in ["Rejected", "Draft"]:
                raise Exception("Syllabus cannot be updated in this state")

            # ✅ UPDATE FILE + RESET STATUS
            self.uow.syllabuses.update_file(
                syllabus_id=syllabus_id,
                file_path=file_path,
                status="Draft")

    def resubmit_syllabus(self, syllabus_id, lecturer_id):
        with self.uow:
            user = self.uow.users.get_by_id(lecturer_id)
            if not user or user.role_code != "LECTURER":
                raise Exception("Only lecturer can resubmit syllabus")

            syllabus = self.uow.syllabuses.get_by_id(syllabus_id)
            if not syllabus:
                raise Exception("Syllabus not found")

            self.uow.syllabuses.update_status(syllabus_id, "PendingReview")

