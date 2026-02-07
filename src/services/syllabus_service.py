from infrastructure.models.syllabus_model import SyllabusModel
from sqlalchemy import func


class SyllabusService:

    def __init__(self, uow):
        self.uow = uow

    def create_syllabus(self, course_id, file_path, lecturer_id):

        with self.uow:

            max_version = (
                self.uow.session
                .query(func.max(SyllabusModel.version_number))
                .filter(SyllabusModel.course_id == course_id)
                .scalar()
            ) or 0

            syllabus = SyllabusModel(
                course_id=course_id,
                version_number=max_version + 1,
                status="Draft",
                file_path=file_path, 
                lecturer_id=lecturer_id
            )

            self.uow.syllabuses.add(syllabus)
            self.uow.commit()
            return syllabus


    # ======================================================
    # LECTURER – SUBMIT SYLLABUS
    # ======================================================
    def submit_syllabus(self, syllabus_id, lecturer_id):
        with self.uow:

            user = self.uow.users.get_by_id(lecturer_id)
            if not user or user.role_code != "LECTURER":
                raise Exception("Only lecturer can submit syllabus")

            syllabus = self.uow.syllabuses.get_by_id(syllabus_id)
            if not syllabus:
                raise Exception("Syllabus not found")

            self.uow.syllabuses.update_status(
                syllabus_id,
                "PendingReview"
            )

