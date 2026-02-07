# src/domain/repositories/base_repository.py

from abc import ABC, abstractmethod


class BaseRepository(ABC):

    @abstractmethod
    def find_by_id(self, id: int):
        pass
