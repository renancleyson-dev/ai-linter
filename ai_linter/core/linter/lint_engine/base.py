import asyncio
from abc import ABC
from typing import TypedDict, Any

from ..prompts.base import Error, Rules
from ..code_search import SupportedLanguages
from ..strategies.rules_classification import RulesClassificationStrategy
from ..strategies.naming_convention import NamingConventionStrategy


class Chunk(TypedDict):
    file: str
    text: str


class BaseLintEngine(ABC):
    llm: Any

    def run(self, chunks: list[Chunk], rules: list[str]) -> dict[str, list[Error]]:
        return asyncio.run(self.arun(chunks, rules))

    async def arun(self, chunks: list[Chunk], rules: list[str]):
        if not (self.llm):
            raise ValueError("No LLM was initialized")

        rules_classification_strategy = RulesClassificationStrategy(self.llm)
        naming_convention_strategy = NamingConventionStrategy(self.llm)
        errors: dict[str, list[Error]] = {chunk["file"]: [] for chunk in chunks}

        labeled_rules = await rules_classification_strategy.arun(rules)
        for chunk in chunks:
            naming_convention_rules = labeled_rules[Rules.NAMING_CONVENTION]

            if naming_convention_rules:
                naming_convention_result = await naming_convention_strategy.arun(
                    rules=naming_convention_rules,
                    chunk=chunk["text"],
                    programming_language=SupportedLanguages.PYTHON,
                )

                errors[chunk["file"]].extend(naming_convention_result)

        return errors
