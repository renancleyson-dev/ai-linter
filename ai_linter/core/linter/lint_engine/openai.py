from typing import Optional, Final
from langchain.llms.base import BaseLLM
from langchain.chat_models import ChatOpenAI

from .base import BaseLintEngine


class OpenAILintEngine(BaseLintEngine):
    MODEL: Final = "gpt-3.5-turbo-0613"
    llm: Optional[BaseLLM] = None

    def set_api_key(self, api_key: str):
        self.llm = ChatOpenAI(
            openai_api_key=api_key,
            model=self.MODEL,
            temperature=0,
            max_tokens=2000,
            model_kwargs={
                "top_p": 0
            }
        )  # type: ignore
