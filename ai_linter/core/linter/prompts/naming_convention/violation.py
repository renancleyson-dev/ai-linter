import json
from typing import TypedDict

from ..base import Prompt, Example


Violation = TypedDict("Violation", {"convention": str, "rule": str})

NO_VIOLATION = "NONE"


INSTRUCTION_TEMPLATE = f"""\
You are AI Linter, an assistant for linting code with rules in English text.

Your task is to identify naming conventions from the given parameter and rules.

The parameters are code chunks extracted from a source code. They are grouped by the following types:
    - variable
    - function
    - class
    - typing

Use the following instructions to complete the task:
    - Search for rules that include the parameter's type
    - If no rule was found, skip the next step and show the output {NO_VIOLATION}
    - For each rule do the following:
        - Identify the chunk's naming convention
        - generate a JSON with the rule and the naming convention of the chunk\
"""

INPUT_TEMPLATE = """\
rules:
{rules}

parameter:
type: {parameter_type}

chunk:
```{programming_language}
{chunk}
```\
"""

EXAMPLES: list[Example] = [
    {
        "question": INPUT_TEMPLATE.format(
            parameter_type="typing",
            chunk="Sequence",
            programming_language="python",
            rules="variables and functions should be snake-case\nclasses should be kebab-case",
        ),
        "answer": NO_VIOLATION,
    },
    {
        "question": INPUT_TEMPLATE.format(
            parameter_type="class",
            chunk="Init",
            programming_language="python",
            rules="variables and functions should be snake-case\nclasses should be kebab-case",
        ),
        "answer": '{{\n  "convention": "pascal-case",\n  "rule": "classes should be kebab-case"\n}}',
    },
    {
        "question": INPUT_TEMPLATE.format(
            parameter_type="class",
            chunk="Run",
            programming_language="python",
            rules="variables and functions should be snake-case\nclasses should be kebab-case",
        ),
        "answer": '{{\n  "convention": "pascal-case",\n  "rule": "classes should be kebab-case" \n}}',
    },
    {
        "question": INPUT_TEMPLATE.format(
            parameter_type="class",
            chunk="Command",
            programming_language="python",
            rules="variables and functions should be snake-case\nclasses should be kebab-case",
        ),
        "answer": '{{\n  "convention": "pascal-case",\n  "rule": "classes should be kebab-case" \n}}',
    },
    {
        "question": INPUT_TEMPLATE.format(
            parameter_type="function",
            chunk="someFunction",
            programming_language="python",
            rules="variables and functions should be snake-case\nclasses should be kebab-case",
        ),
        "answer": '{{\n  "convention": "camel-case",\n  "rule": "variables and functions should be snake-case" \n}}',
    },
]


def parse(value: str) -> Violation | None:
    if value == NO_VIOLATION:
        return None

    return json.loads(value)


violation_prompt = Prompt(
    input=INPUT_TEMPLATE,
    instruction=INSTRUCTION_TEMPLATE,
    examples=EXAMPLES,
    parse=parse,
)
