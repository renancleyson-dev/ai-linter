from ai_linter.core.linter.ai_engine import OpenAILintEngine
from ai_linter.core.storage import LocalRepositoryStorage
from ai_linter.core.storage import LocalConfigurationStorage
from ai_linter.core.models import Repository
from ai_linter.core.linter import Linter

LintEngine = OpenAILintEngine()
RepositoryStorage = LocalRepositoryStorage()
ConfigurationStorage = LocalConfigurationStorage()

Repository.set_dependencies(RepositoryStorage=RepositoryStorage)
Linter.set_dependencies(LintEngine=LintEngine, RepositoryStorage=RepositoryStorage)
