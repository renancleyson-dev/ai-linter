from abc import ABC, abstractmethod


class BaseRepositoryStorage(ABC):
    @abstractmethod
    def get_file_data(self, file_path) -> str | None:
        pass


class LocalRepositoryStorage(BaseRepositoryStorage):
    def get_file_data(self, file_path):
        with open(file_path) as local_file:
            data = local_file.read()
            if data:
                return data
