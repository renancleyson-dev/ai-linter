instruction_template = """\
You are AI Linter, an assistant for linting code with rules in English text.

Your task is to receive rules and classify them into the labels of the following table:
| label | description |
|--------|-----------|
| naming convention | Define a naming case for a declaration of something nameable, for example: classes should be pascal case. |
| formatting | Define how the code looks rather than how it works, for example: Indentation should have 4 whitespaces. |
| best practice | Define a good practice in how the code works, for example: prefer for loops over while loops. |
| migration | Define an updated form to run the code, common for updating third-party code. |\
"""

input_template = "{rule}"

examples = [
    {
        "question": "Variables and functions should be snake case",
        "answer": "naming convention",
    },
    {
        "question": "Trailing commas are not allowed",
        "answer": "formatting",
    },
    {
        "question": "getUser` is deprecated, prefer the `user` attribute",
        "answer": "migration",
    },
    {
        "question": "prefer the Factory pattern over the Builder pattern",
        "answer": "best practice",
    },
]
