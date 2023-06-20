from tree_sitter import Language, Parser, Tree, Node
from abc import ABC, abstractmethod
from enum import StrEnum
from typing import TypedDict, Final, NotRequired, Optional


ParseParameter = TypedDict(
    "ParseParameter",
    {
        "chunk": str,
        "type": str,
        "line": int,
        "start-column": int,
        "end-column": int,
        "extra": NotRequired[dict[str, str]],
    },
)


class SupportedLanguages(StrEnum):
    PYTHON = "python"


class BaseCodeSearch(ABC):
    LIBRARY_PATH: Final = "scripts/tree-sitter/build/languages.so"
    tree: Tree
    language: Language

    def __init__(self, chunk: str, programming_language: SupportedLanguages):
        self.language = Language(self.LIBRARY_PATH, programming_language)
        parser = Parser()
        parser.set_language(self.language)

        self.tree = parser.parse(bytes(chunk, "utf-8"))

    def query(
        self, search: str, filter_by: Optional[list[str]] = None
    ) -> list[ParseParameter]:
        lang_query = self.language.query(search)

        captures = lang_query.captures(self.tree.root_node)
        result = []
        for node, name in captures:
            if filter_by == None or name in filter_by:
                result.append(self._node_to_parameter(node))

        return result

    @abstractmethod
    def get_functions(self, function_name="") -> list[ParseParameter]:
        pass

    @abstractmethod
    def get_variables(self, variable_name="", variable_type="") -> list[ParseParameter]:
        pass

    @abstractmethod
    def get_classes(self, class_name="", class_parent="") -> list[ParseParameter]:
        pass

    @abstractmethod
    def get_constants(self, constant_name="", constant_type="") -> list[ParseParameter]:
        pass

    @abstractmethod
    def get_types(self, type_name="") -> list[ParseParameter]:
        pass

    @staticmethod
    def _node_to_parameter(node: Node, extra: dict[str, str] = {}) -> ParseParameter:
        return {
            "chunk": node.text.decode(),
            "type": node.type,
            "line": node.start_point[0],
            "start-column": node.start_point[1],
            "end-column": node.end_point[1],
            "extra": extra,
        }
