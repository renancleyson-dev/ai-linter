INSTRUCTION_TEMPLATE = """\
You are AI Linter, an assistant for linting code with rules in English text.

Your task is to identify naming conventions from the given parameter and rules.

The parameters are code chunks extracted from a source code. They are grouped by the following types:
    - variable
    - function
    - class
    - typing

Use the following instructions to complete the task:
    - Search for rules that include the parameter's type
    - If no rule was found, skip the next step and show the output "NONE"
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

EXAMPLES = [
    {
        "question": INPUT_TEMPLATE.format(
            parameter_type="typing",
            chunk="Sequence",
            programming_language="python",
            rules="variables and functions should be snake-case\nclasses should be kebab-case",
        ),
        "answer": "NONE",
    },
    {
        "question": INPUT_TEMPLATE.format(
            parameter_type="class",
            chunk="Init",
            programming_language="python",
            rules="variables and functions should be snake-case\nclasses should be kebab-case",
        ),
        "answer": '{{\n"naming-convention": "pascal-case", "rule": "classes should be kebab-case"\n}}',
    },
    {
        "question": INPUT_TEMPLATE.format(
            parameter_type="class",
            chunk="Run",
            programming_language="python",
            rules="variables and functions should be snake-case\nclasses should be kebab-case",
        ),
        "answer": '{{\n"naming-convention": "pascal-case", "rule": "classes should be kebab-case" \n}}',
    },
    {
        "question": INPUT_TEMPLATE.format(
            parameter_type="class",
            chunk="Command",
            programming_language="python",
            rules="variables and functions should be snake-case\nclasses should be kebab-case",
        ),
        "answer": '{{\n"naming-convention": "pascal-case", "rule": "classes should be kebab-case" \n}}',
    },
    {
        "question": INPUT_TEMPLATE.format(
            parameter_type="function",
            chunk="someFunction",
            programming_language="python",
            rules="variables and functions should be snake-case\nclasses should be kebab-case",
        ),
        "answer": '{{\n"naming-convention": "camel-case", "rule": "variables and functions should be snake-case" \n}}',
    },
]
