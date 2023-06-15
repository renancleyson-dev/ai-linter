from ..base import Prompt, Example

INSTRUCTION_TEMPLATE = """\
You are AI Linter, an assistant for linting code with rules in English text.

Your task is to receive code chunks and convert them into plain text, then \
convert the generated plain text into a code chunk with the linting rules applied.

Here's a simple representation of the procedure:
code chunk -> plain text -> code chunk with rules applied.

Use the following instructions to complete the task:
    - For each code chunk:
        - Supposing that there's a single rule "variables should be camel-case" and a chunk "some_var"
        - Convert the code chunk into a plain text form by capturing the words in the chunk: "some_var" -> "some var"
        - Convert the generated plain text into a code chunk with the rules applied: "some var" -> "someVar"
    - Finally, show the output with the original chunk and generated chunk.\
"""

INPUT_TEMPLATE = """\
rules:
{rules}

```{programming_language}
{chunk}
```\
"""

EXAMPLES: list[Example] = [
    {
        "question": INPUT_TEMPLATE.format(
            programming_language="python",
            chunk="some_variable",
            rules="variables should be kebab-case",
        ),
        "answer": "some-variable",
    },
    {
        "question": INPUT_TEMPLATE.format(
            programming_language="python",
            chunk="getItem",
            rules="functions should be camel-case",
        ),
        "answer": "getItem",
    },
    {
        "question": INPUT_TEMPLATE.format(
            programming_language="python",
            chunk="Handler",
            rules="classes should be snake case",
        ),
        "answer": "handler",
    },
    {
        "question": INPUT_TEMPLATE.format(
            programming_language="python",
            chunk="start_date",
            rules="variables should be pascal-case",
        ),
        "answer": "StartDate",
    },
    {
        "question": INPUT_TEMPLATE.format(
            programming_language="python",
            chunk="find_user",
            rules="methods should be camel-case",
        ),
        "answer": "findUser",
    },
]

fix_prompt = Prompt(
    input=INPUT_TEMPLATE,
    instruction=INSTRUCTION_TEMPLATE,
    examples=EXAMPLES,
    parse=lambda value: value
)
