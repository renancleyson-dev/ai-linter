from typing import cast
from langchain.chains import LLMChain
from langchain.llms.base import BaseLLM
from langchain.prompts.base import BasePromptTemplate
from langchain.prompts.chat import (
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
    ChatPromptTemplate,
)
from langchain.prompts.few_shot_with_templates import FewShotPromptWithTemplates
from langchain.prompts.prompt import PromptTemplate

from ..prompts.base import Prompt

EXAMPLE_TEMPLATE = """\
USER:
{question}

ASSISTANT:
{answer}\
"""

PREFIX_TEMPLATE = """\
{instruction}

=========== EXAMPLES ===========
"""

BASE_SUFFIX_TEMPLATE = """
=========== END OF EXAMPLES ===========
"""

SUFFIX_TEMPLATE = (
    BASE_SUFFIX_TEMPLATE
    + """

USER:
{input}

ASSISTANT:
"""
)


def create_chain_from_prompt(llm: BaseLLM, prompt: Prompt, is_chat=False):
    input_variables: list[str] = []
    full_prompt: BasePromptTemplate | None = None
    instruction_prompt = None

    examples = cast(list[dict], prompt.examples)
    example_prompt = PromptTemplate.from_template(EXAMPLE_TEMPLATE)

    if prompt.instruction:
        instruction_prompt = PromptTemplate.from_template(
            PREFIX_TEMPLATE.format(instruction=prompt.instruction)
        )

        input_variables.extend(instruction_prompt.input_variables)

    if is_chat:
        suffix_prompt = PromptTemplate.from_template(BASE_SUFFIX_TEMPLATE)
        human_message_prompt = HumanMessagePromptTemplate.from_template(prompt.input)

        system_message_prompt = SystemMessagePromptTemplate(
            prompt=FewShotPromptWithTemplates(
                prefix=instruction_prompt,
                suffix=suffix_prompt,
                example_prompt=example_prompt,
                examples=examples,
                input_variables=input_variables,
            )
        )

        full_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )
    else:
        entry_prompt = PromptTemplate.from_template(
            SUFFIX_TEMPLATE.format(input=prompt.input)
        )
        input_variables.extend(entry_prompt.input_variables)

        full_prompt = FewShotPromptWithTemplates(
            prefix=instruction_prompt,
            suffix=entry_prompt,
            example_prompt=example_prompt,
            examples=examples,
            input_variables=input_variables,
        )

    return LLMChain(
        llm=llm,
        prompt=full_prompt,
    )
