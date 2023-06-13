import asyncio
from typing import Optional, Final
from langchain.llms import OpenAI

from .base import BaseLintEngine


class OpenAILintEngine(BaseLintEngine):
    MODEL: Final = "gpt-3.5-turbo"
    llm: Optional[OpenAI] = None

    def set_api_key(self, api_key: str):
        self.llm = OpenAI(
            openai_api_key=api_key,
            model=self.MODEL,
            model_kwargs={
                "temperature": 0,
                "top_p": 0,
                "max_tokens": 2000,
            },
        )  # type: ignore

    def run(self, chunks, rules):
        return asyncio.run(self.arun(chunks, rules))
