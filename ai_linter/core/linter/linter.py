import os.path
from typing import ClassVar

from ai_linter.core.models import Repository, is_file
from ai_linter.core.storage import RepositoryStorageABC, Configuration
from .ai_engine import LintEngineABC, Chunk


class Linter:
    RepositoryStorage: ClassVar[RepositoryStorageABC]
    LintEngine: ClassVar[LintEngineABC]

    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.conditions = [rule["condition"] for rule in self.configuration["rules"]]

    @classmethod
    def set_dependencies(
        cls,
        LintEngine: LintEngineABC,
        RepositoryStorage: RepositoryStorageABC,
    ):
        cls.LintEngine = LintEngine
        cls.RepositoryStorage = RepositoryStorage

    def lint_by_file(self, file_path: str):
        text = self.RepositoryStorage.get_file_data(file_path)

        if not text:
            raise FileNotFoundError

        chunk: Chunk = {
            "file": file_path,
            "text": text,
        }

        return self.LintEngine.lint(chunks=[chunk], rules=self.conditions)

    def lint_by_repository(self, repository: Repository):
        chunks: list[Chunk] = []

        for directory in repository:
            for child in directory.children:
                if is_file(child):
                    text = self.RepositoryStorage.get_file_data(child.path)

                    if text:
                        chunk: Chunk = {"file": child.path, "text": text}
                        chunks.append(chunk)

        return self.LintEngine.lint(chunks=chunks, rules=self.conditions)
