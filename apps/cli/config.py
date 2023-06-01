import os
import dotenv
import openai

from core.common.ai_engine import OpenAILintEngine
from core.common.storage import LocalRepositoryStorage
from core.common.storage import LocalConfigurationStorage
from core.common.models import Repository
from core.linter import Linter

LintEngine = OpenAILintEngine()
RepositoryStorage = LocalRepositoryStorage()
ConfigurationStorage = LocalConfigurationStorage()

Repository.set_dependencies(LintEngine=LintEngine, RepositoryStorage=RepositoryStorage)
Linter.set_dependencies(LintEngine=LintEngine, RepositoryStorage=RepositoryStorage)
