from domain.models.syllabus import Syllabus

class SyllabusService:

    def __init__(
        self,
        syllabus_repository,
        file_storage_service,
        unit_of_work
    ):
        self.syllabus_repository = syllabus_repository
        self.file_storage_service = file_storage_service
        self.uow = unit_of_work

    def upload_syllabus(self, command):
        try:
            # 1. save file
            file_path = self.file_storage_service.save_file(command["file"])

            # 2. create entity
            syllabus = Syllabus(
                file_path=file_path,
                course_id=command["course_id"],
                lecture_id=command["lecture_id"]
            )

            # 3. save db
            self.syllabus_repository.add(syllabus)

            # 4. commit
            self.uow.commit()

            return True

        except Exception as e:
            self.uow.rollback()
            raise e
