class FeedbackService:

    def __init__(self, uow):
        self.uow = uow

    def send_feedback(self, student_id, syllabus_id, content):
        self.uow.syllabus_repo.save_feedback(
            student_id,
            syllabus_id,
            content
        )
        self.uow.commit()
