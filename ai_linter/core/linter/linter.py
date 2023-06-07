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

    @classmethod
    def set_dependencies(
        cls,
        LintEngine: LintEngineABC,
        RepositoryStorage: RepositoryStorageABC,
    ):
        cls.LintEngine = LintEngine
        cls.RepositoryStorage = RepositoryStorage

    def lint_by_file(self, chunk: Chunk, rules: list[str]):
        return self.LintEngine.lint(chunks=[chunk], rules=rules)

    def lint_by_repository(self, repository: Repository):
        chunks: list[Chunk] = []
        rules = [rule["condition"] for rule in self.configuration["rules"]]

        for directory in repository:
            for child in directory.children:
                if not is_file(child):
                    continue

                path = os.path.join(child.parent.path, child.name)
                text = self.RepositoryStorage.get_file_data(path)

                if text:
                    chunk: Chunk = {"file": path, "text": text}
                    chunks.append(chunk)

        return self.LintEngine.lint(chunks=chunks, rules=rules)
