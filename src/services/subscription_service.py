class SubscriptionService:

    def __init__(self, uow):
        self.uow = uow

    def subscribe(self, student_id: int, syllabus_id: int):
        self.uow.syllabus_repo.save_subscription(student_id, syllabus_id)
        self.uow.commit()
