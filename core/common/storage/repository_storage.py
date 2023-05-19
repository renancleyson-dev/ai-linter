from abc import ABC, abstractmethod
from typing import Any


class RepositoryStorageABC(ABC):
    @abstractmethod
    def get_file_data(self, file_path) -> str | None:
        pass


class LocalRepositoryStorage(RepositoryStorageABC):
    def get_file_data(self, file_path):
        with open(file_path) as local_file:
            data = local_file.read()
            if data:
                return data
