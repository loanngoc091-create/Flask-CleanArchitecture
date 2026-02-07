class StudentSyllabusService:

    def __init__(self, uow):
        self.uow = uow

    def get_published_syllabi(self):
        with self.uow as uow:
            return uow.syllabuses.get_published()
        
    def get_published_detail(self, syllabus_id: int):
        with self.uow as uow:
            syllabus = uow.syllabuses.get_published_detail(syllabus_id)

            if not syllabus:
                raise Exception("Syllabus not found")

            return syllabus
    
    def get_published_detail(self, syllabus_id):
        with self.uow as uow:
            syllabus = uow.syllabuses.get_published_detail(syllabus_id)

            if not syllabus:
                raise Exception("Syllabus not found")

            return syllabus