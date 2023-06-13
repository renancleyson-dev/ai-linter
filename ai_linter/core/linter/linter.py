from typing import ClassVar

from ai_linter.core.models.repository import Repository, is_file
from ai_linter.core.storage import BaseRepositoryStorage
from ai_linter.core.storage.configuration_storage import Configuration

from .lint_engine.base import BaseLintEngine, Chunk


class Linter:
    repository_storage: ClassVar[BaseRepositoryStorage]
    lint_engine: ClassVar[BaseLintEngine]

    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.conditions = [rule["condition"] for rule in self.configuration["rules"]]

    @classmethod
    def set_dependencies(
        cls,
        lint_engine: BaseLintEngine,
        repository_storage: BaseRepositoryStorage,
    ):
        cls.lint_engine = lint_engine
        cls.repository_storage = repository_storage

    def lint_by_file(self, file_path: str):
        text = self.repository_storage.get_file_data(file_path)

        if not text:
            raise RuntimeError(f"The file {file_path} is empty")

        chunk: Chunk = {
            "file": file_path,
            "text": text,
        }

        return self.lint_engine.run(chunks=[chunk], rules=self.conditions)

    def lint_by_repository(self, repository: Repository):
        chunks: list[Chunk] = []

        for directory in repository:
            for child in directory.children:
                if is_file(child):
                    text = self.repository_storage.get_file_data(child.path)

                    if text:
                        chunk: Chunk = {"file": child.path, "text": text}
                        chunks.append(chunk)

        return self.lint_engine.run(chunks=chunks, rules=self.conditions)
