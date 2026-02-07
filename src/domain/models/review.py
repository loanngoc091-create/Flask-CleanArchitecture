from datetime import datetime

class Review:
    def __init__(self, syllabus_id, decision, comment, reviewer_id):
        self.syllabus_id = syllabus_id
        self.decision = decision          # APPROVED | REJECTED
        self.comment = comment
        self.reviewer_id = reviewer_id
        self.review_date = datetime.utcnow()
