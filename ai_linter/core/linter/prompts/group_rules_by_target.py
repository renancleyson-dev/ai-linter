import json
from typing import cast

from .base import Prompt, Example


GroupedRules = dict[str, list[str]]


INSTRUCTION_TEMPLATE = """\
You are AI Linter, an assistant for linting code with rules in English text.

Each rule has a target. Your task is to group the provided rules with their targets.
"""

INPUT_TEMPLATE = "{rules}"


def create_output(value: GroupedRules):
    return json.dumps(value, indent=2).replace("{", "{{").replace("}", "}}")


EXAMPLES: list[Example] = [
    {
        "question": INPUT_TEMPLATE.format(
            rules="\n".join(
                ["variables should be snake-case", "classes should be pascal-case"]
            )
        ),
        "answer": create_output(
            {
                "classes": ["classes should be pascal-case"],
                "variables": ["variables should be snake-case"],
            },
        ),
    },
    {
        "question": INPUT_TEMPLATE.format(
            rules="\n".join(
                ["types should end with the letter T", "types should be pascal-case"]
            )
        ),
        "answer": create_output(
            {
                "types": [
                    "types should end with the letter T",
                    "types should be pascal-case",
                ],
            }
        ),
    },
    {
        "question": INPUT_TEMPLATE.format(
            rules="\n".join(
                [
                    "constants should be screaming snake-case",
                    "functions should be pascal-case",
                ]
            )
        ),
        "answer": create_output(
            {
                "constants": ["constants should be screaming snake-case"],
                "functions": ["function should be camel-case"],
            }
        ),
    },
]


def parse(value: str):
    return cast(GroupedRules, json.loads(value))


group_rules_prompt = Prompt(
    input=INPUT_TEMPLATE,
    instruction=INSTRUCTION_TEMPLATE,
    examples=EXAMPLES,
    parse=parse,
)
