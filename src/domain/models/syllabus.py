from datetime import datetime


class Syllabus:

    def __init__(
        self,
        syllabus_id: int | None = None,
        version_number: int = 1,
        status: str = "Draft",
        course_id: int | None = None
    ):
        self.syllabus_id = syllabus_id
        self.version_number = version_number
        self.status = status
        self.course_id = course_id 

        self.created_date = datetime.utcnow()
        self.updated_date = None

    # ======================
    # DOMAIN BEHAVIORS
    # ======================

    def submit(self):
        if self.status != "Draft":
            raise Exception("Only Draft syllabus can be submitted")
        self.status = "PendingReview"

    def approve(self):
        if self.status != "PendingReview":
            raise Exception("Only Pending syllabus can be approved")
        self.status = "Approved"

    def reject(self):
        if self.status != "PendingReview":
            raise Exception("Only Pending syllabus can be rejected")
        self.status = "Rejected"

    def revise(self):
        if self.status != "Rejected":
            raise Exception("Only Rejected syllabus can be revised")

        self.version_number += 1
        self.status = "Draft"
        self.updated_date = datetime.utcnow()

    def final_approve(self):
        if self.status != "Approved":
            raise Exception("Syllabus must be approved before final approval")

        self.status = "FinalApproved"
