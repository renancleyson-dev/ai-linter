from typing import TypedDict
import textwrap


class RuleLabel(TypedDict):
    name: str
    description: str


RULE_LABELS: list[RuleLabel] = [
    {
        "name": "naming-convention",
        "description": "Define a naming case for a declaration of something nameable, for example: classes should be pascal case.",
    },
    {
        "name": "formatting",
        "description": "Define how the code looks rather than how it works, for example: Indentation should have 4 whitespaces.",
    },
    {
        "name": "best-practice",
        "description": "Define a good practice in how the code works, for example: prefer for loops over while loops.",
    },
    {
        "name": "migration",
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

EXAMPLES = [
    {
        "question": "Variables and functions should be snake case",
        "answer": "naming-convention",
    },
    {
        "question": "Trailing commas are not allowed",
        "answer": "formatting",
    },
    {
        "question": "`getUser` is deprecated, prefer the `user` attribute",
        "answer": "migration",
    },
    {
        "question": "prefer the Factory pattern over the Builder pattern",
        "answer": "best-practice",
    },
]
