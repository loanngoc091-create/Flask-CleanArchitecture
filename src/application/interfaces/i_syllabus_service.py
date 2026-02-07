# application/interfaces/i_syllabus_service.py
from abc import ABC, abstractmethod

class ISyllabusService(ABC):

    @abstractmethod
    def upload_syllabus(self, command):
        pass
