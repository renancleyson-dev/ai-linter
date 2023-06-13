from abc import ABC, abstractmethod
from typing import TypedDict, Any

from ..prompts.base import Error, Rules
from ..strategies.rules_classification import handle_rules_classification
from ..strategies.naming_convention import  handle_naming_convention


class Chunk(TypedDict):
    file: str
    text: str


class BaseLintEngine(ABC):
    llm: Any

    async def arun(self, chunks: list[Chunk], rules: list[str]):
        if not (self.llm):
            raise ValueError("No LLM was initialized")

        errors: dict[str, list[Error]] = {chunk["file"]: [] for chunk in chunks}

        labeled_rules = await handle_rules_classification(self.llm, rules)
        for chunk in chunks:
            naming_convention_rules = labeled_rules[Rules.NAMING_CONVENTION]
            naming_convention_result = await handle_naming_convention(
                llm=self.llm, rules=naming_convention_rules, chunk=chunk["text"]
            )

            errors[chunk["file"]].extend(naming_convention_result)

        return errors

    @abstractmethod
    def run(self, chunks: list[Chunk], rules: list[str]) -> dict[str, list[Error]]:
        pass
