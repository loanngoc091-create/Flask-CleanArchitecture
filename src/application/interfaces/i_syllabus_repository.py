from abc import ABC, abstractmethod

class ISyllabusRepository(ABC):

    @abstractmethod
    def add(self, syllabus):
        pass

    @abstractmethod
    def find_by_course(self, course_id: int):
        pass
