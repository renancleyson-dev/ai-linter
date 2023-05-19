import os
import dotenv
import openai

from core.common.ai_engine import OpenAILintEngine
from core.common.storage import LocalRepositoryStorage
from core.common.storage import LocalConfigurationStorage
from core.common.models import Repository
from core.linter import Linter

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

LintEngine = OpenAILintEngine()
RepositoryStorage = LocalRepositoryStorage()
ConfigurationStorage = LocalConfigurationStorage()

Repository.set_dependencies(LintEngine=LintEngine, RepositoryStorage=RepositoryStorage)
Linter.set_dependencies(LintEngine=LintEngine, RepositoryStorage=RepositoryStorage)
