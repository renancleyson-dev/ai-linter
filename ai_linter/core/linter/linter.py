from typing import ClassVar

from ai_linter.core.models import Repository, is_file
from ai_linter.core.storage import BaseRepositoryStorage, Configuration
from .ai_engine import BaseLintEngine, Chunk


class Linter:
    repositoryStorage: ClassVar[BaseRepositoryStorage]
    lintEngine: ClassVar[BaseLintEngine]

    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.conditions = [rule["condition"] for rule in self.configuration["rules"]]

    @classmethod
    def set_dependencies(
        cls,
        lintEngine: BaseLintEngine,
        repositoryStorage: BaseRepositoryStorage,
    ):
        cls.lintEngine = lintEngine
        cls.repositoryStorage = repositoryStorage

    def lint_by_file(self, file_path: str):
        text = self.repositoryStorage.get_file_data(file_path)

        if not text:
            raise FileNotFoundError

        chunk: Chunk = {
            "file": file_path,
            "text": text,
        }

        return self.lintEngine.lint(chunks=[chunk], rules=self.conditions)

    def lint_by_repository(self, repository: Repository):
        chunks: list[Chunk] = []

        for directory in repository:
            for child in directory.children:
                if is_file(child):
                    text = self.repositoryStorage.get_file_data(child.path)

                    if text:
                        chunk: Chunk = {"file": child.path, "text": text}
                        chunks.append(chunk)

        return self.lintEngine.lint(chunks=chunks, rules=self.conditions)
