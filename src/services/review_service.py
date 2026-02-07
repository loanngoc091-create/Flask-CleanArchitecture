from domain.models.review import Review

class ReviewService:

    def __init__(self, uow):
        self.uow = uow

    def review_syllabus(self, command):

        syllabus_id = command["syllabus_id"]
        decision = command["decision"]
        reviewer_id = command["reviewer_id"]
        comment = command.get("comment", "")

        syllabus = self.uow.syllabus_repo.get_by_id(syllabus_id)

        if not syllabus:
            raise Exception("Syllabus not found")

        if decision == "APPROVED":
            syllabus.status = "APPROVED"
        else:
            syllabus.status = "REJECTED"

        review = Review(
            syllabus_id=syllabus_id,
            decision=decision,
            comment=comment,
            reviewer_id=reviewer_id
        )

        self.uow.review_repo.add(review)
        self.uow.commit()
