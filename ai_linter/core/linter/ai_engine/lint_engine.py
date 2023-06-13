import asyncio
from abc import ABC, abstractmethod
from typing import TypedDict, Optional, Final
from langchain.llms.base import BaseLLM
from langchain.llms import OpenAI

from ..prompts.base import Error, Rules
from ..strategies.naming_convention import handle_naming_convention
from ..strategies.rules_classification import handle_rules_classification


class Chunk(TypedDict):
    file: str
    text: str


class BaseLintEngine(ABC):
    @abstractmethod
    def run(self, chunks: list[Chunk], rules: list[str]) -> dict[str, list[Error]]:
        pass


class OpenAILintEngine(BaseLintEngine):
    llm: Optional[BaseLLM] = None

    def set_api_key(self, api_key: str):
        self.llm = OpenAI(
            openai_api_key=api_key,
            model=self.MODEL,
            temperature=0,
            top_p=0,
            max_tokens=2000,
        )  # type: ignore

    async def arun(self, chunks: list[Chunk], rules: list[str]):
        if not (self.llm):
            raise ValueError("OpenAI API key is required")

        errors: dict[str, list[Error]] = {chunk["file"]: [] for chunk in chunks}

        labeled_rules = await handle_rules_classification(self.llm, rules)
        for chunk in chunks:
            naming_convention_rules = labeled_rules[Rules.NAMING_CONVENTION]
            naming_convention_result = await handle_naming_convention(
                llm=self.llm, rules=naming_convention_rules, chunk=chunk["text"]
            )

            errors[chunk["file"]].extend(naming_convention_result)

        return errors

    def run(self, chunks, rules):
        return asyncio.run(self.arun(chunks, rules))

    MODEL: Final = "text-davinci-003"
