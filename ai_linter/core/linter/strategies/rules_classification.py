import asyncio
from langchain.llms.base import BaseLLM
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

from ..prompts.rules_classification import rule_classification_prompt
from ..prompts.base import Rules
from ..adapters.langchain import create_chain_from_prompt


class RulesClassificationStrategy:
    llm: BaseLLM
    rule_classification_chain: LLMChain

    def __init__(self, llm: BaseLLM):
        is_chat = isinstance(llm, ChatOpenAI)

        self.llm = llm
        self.rule_classification_chain = create_chain_from_prompt(
            llm=llm, prompt=rule_classification_prompt, is_chat=is_chat
        )

    def run(self, rules: list[str]):
        asyncio.run(self.arun(rules))

    async def arun(self, rules: list[str]):
        labeled_rules: dict[str, list[str]] = {label: [] for label in Rules}

        coros = [self._handle_rule(rule) for rule in rules]
        for coro in asyncio.as_completed(coros):
            label, rule = await coro
            labeled_rules[label].append(rule)

        return labeled_rules
    
    async def _handle_rule(self, rule: str):
            label = rule_classification_prompt.parse(
                await self.rule_classification_chain.arun(rule=rule)
            )

            return (label, rule)
