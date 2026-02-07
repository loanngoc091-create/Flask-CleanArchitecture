class Approval:

    def __init__(
        self,
        syllabus_id: int,
        status: str,
        step: int,
        role_id: int,
        user_id: int
    ):
        self.syllabus_id = syllabus_id
        self.status = status
        self.step = step
        self.role_id = role_id
        self.user_id = user_id
        