from .base import BaseCodeSearch, SupportedLanguages, ParseParameter
from .python_code_search import PythonCodeSearch


def create_code_search(chunk: str, programming_language: SupportedLanguages):
    CODE_SEARCH_CLASSES = {SupportedLanguages.PYTHON: PythonCodeSearch}

    try:
        return CODE_SEARCH_CLASSES[programming_language](chunk, programming_language)
    except KeyError:
        raise RuntimeError(f"The {programming_language} language isn't supported")
