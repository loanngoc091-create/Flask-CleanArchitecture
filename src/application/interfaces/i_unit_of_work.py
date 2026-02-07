from abc import ABC, abstractmethod

class IUnitOfWork(ABC):

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass
