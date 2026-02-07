class PublishService:

    def __init__(self, uow):
        self.uow = uow

    def publish(self, syllabus_id, user_id):

        with self.uow:

            user = self.uow.users.get_by_id(user_id)
            if user.role_code != "ACADEMIC_AFFAIRS":
                raise Exception("Only Academic Affairs can publish")

            syllabus = self.uow.syllabuses.get_by_id(syllabus_id)
            if syllabus.status != "Approved":
                raise Exception("Syllabus not ready to publish")

            self.uow.syllabuses.update_status(
                syllabus_id,
                "Published"
            )
