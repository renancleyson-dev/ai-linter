from typing import cast
from langchain.chains import LLMChain
from langchain.llms.base import BaseLLM
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

SUFFIX_TEMPLATE = """

=========== END OF EXAMPLES ===========

USER:
{input}

ASSISTANT:
"""


def create_chain_from_prompt(
    llm: BaseLLM,
    prompt: Prompt,
):
    input_variables: list[str] = []
    examples = cast(list[dict], prompt.examples)
    instruction_prompt = None

    example_prompt = PromptTemplate.from_template(EXAMPLE_TEMPLATE)
    entry_prompt = PromptTemplate.from_template(
        SUFFIX_TEMPLATE.format(input=prompt.input)
    )

    input_variables.extend(entry_prompt.input_variables)

    if prompt.instruction:
        instruction_prompt = PromptTemplate.from_template(
            PREFIX_TEMPLATE.format(instruction=prompt.instruction)
        )

        input_variables.extend(instruction_prompt.input_variables)

    return LLMChain(
        llm=llm,
        prompt=FewShotPromptWithTemplates(
            prefix=instruction_prompt,
            suffix=entry_prompt,
            example_prompt=example_prompt,
            examples=examples,
            input_variables=input_variables,
        ),
        verbose=True,
    )
