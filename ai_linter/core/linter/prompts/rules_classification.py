from typing import TypedDict
from langchain.output_parsers.enum import EnumOutputParser
import textwrap

from .base import Rules, Prompt, Example


class RuleLabel(TypedDict):
    name: Rules
    description: str


RULE_LABELS: list[RuleLabel] = [
    {
        "name": Rules.NAMING_CONVENTION,
        "description": "Define a naming case for a declaration of something nameable, for example: classes should be pascal case.",
    },
    {
        "name": Rules.FORMATTING,
        "description": "Define how the code looks rather than how it works, for example: Indentation should have 4 whitespaces.",
    },
    {
        "name": Rules.BEST_PRACTICE,
        "description": "Define a good practice in how the code works, for example: prefer for loops over while loops.",
    },
    {
        "name": Rules.MIGRATION,
        "description": "Define an updated form to run the code, common for updating third-party code.",
    },
]


def labels_to_table():
    rows = []
    ROW_TEMPLATE = "| {label} | {description} |"
    TABLE_TEMPLATE = textwrap.dedent(
        """
        | label | description |
        |-------|-------------|
        {rows}
        """
    )

    for rule in RULE_LABELS:
        rows.append(
            ROW_TEMPLATE.format(label=rule["name"], description=rule["description"])
        )

    return TABLE_TEMPLATE.format(rows="\n".join(rows))


INSTRUCTION_TEMPLATE = f"""\
You are AI Linter, an assistant for linting code with rules in English text.

Your task is to receive rules and classify them into the labels of the following \
markdown table:
{labels_to_table()}\
"""

INPUT_TEMPLATE = "{rule}"

EXAMPLES: list[Example] = [
    {
        "question": "Variables and functions should be snake case",
        "answer": Rules.NAMING_CONVENTION,
    },
    {
        "question": "Trailing commas are not allowed",
        "answer": Rules.FORMATTING,
    },
    {
        "question": "`getUser` is deprecated, prefer the `user` attribute",
        "answer": Rules.MIGRATION,
    },
    {
        "question": "prefer the Factory pattern over the Builder pattern",
        "answer": Rules.BEST_PRACTICE,
    },
]


def parse(value: str) -> Rules:
    return EnumOutputParser(enum=Rules).parse(value)


rule_classification_prompt = Prompt(
    input=INPUT_TEMPLATE,
    instruction=INSTRUCTION_TEMPLATE,
    examples=EXAMPLES,
    parse=parse,
)
