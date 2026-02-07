from abc import ABC, abstractmethod

class IFileStorageService(ABC):

    @abstractmethod
    def save_file(self, file):
        pass

    @abstractmethod
    def delete_file(self, path: str):
        pass
