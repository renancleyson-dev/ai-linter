from langchain.llms.base import BaseLLM
from langchain.llms import OpenAIChat

from ..prompts.rules_classification import rule_classification_prompt
from ..prompts.base import Rules
from ..adapters.langchain import create_chain_from_prompt


async def handle_rules_classification(llm: BaseLLM, rules: list[str]):
    is_chat = isinstance(llm, OpenAIChat)
    labeled_rules: dict[str, list[str]] = {label: [] for label in Rules}
    rule_classification_chain = create_chain_from_prompt(
        llm, rule_classification_prompt, is_chat
    )

    for rule in rules:
        label = rule_classification_prompt.parse(
            await rule_classification_chain.arun(rule=rule)
        )

        labeled_rules[label].append(rule)

    return labeled_rules
