from ai_linter.core.linter.ai_engine import OpenAILintEngine
from ai_linter.core.storage import LocalRepositoryStorage
from ai_linter.core.storage import LocalConfigurationStorage
from ai_linter.core.models import Repository
from ai_linter.core.linter import Linter

lintEngine = OpenAILintEngine()
repositoryStorage = LocalRepositoryStorage()
configurationStorage = LocalConfigurationStorage()

Linter.set_dependencies(lintEngine=lintEngine, repositoryStorage=repositoryStorage)
