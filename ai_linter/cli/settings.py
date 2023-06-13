from ai_linter.core.linter.lint_engine import OpenAILintEngine
from ai_linter.core.linter import Linter
from ai_linter.core.storage import LocalRepositoryStorage
from ai_linter.core.storage import LocalConfigurationStorage

lint_engine = OpenAILintEngine()
repository_storage = LocalRepositoryStorage()
configuration_storage = LocalConfigurationStorage()

Linter.set_dependencies(lint_engine=lint_engine, repository_storage=repository_storage)
