from abc import ABC, abstractmethod
from typing import TypedDict
import textwrap
import openai


class Error(TypedDict):
    message: str
    line: int
    start_column: int
    end_column: int


class Message(TypedDict):
    role: str
    content: str


class Chunk(TypedDict):
    file: str
    text: str


class LintEngineABC(ABC):
    @abstractmethod
    def lint(self, chunks: list[Chunk], rules: list[str]) -> dict[str, list[Error]]:
        pass


class OpenAILintEngine(LintEngineABC):
    model = "gpt-3.5-turbo"
    prompt_template = "RULES:\n{rules}\n\nLint the following code:\n\n```python\n{chunk}\n```"

    @staticmethod
    def format_lines(chunk: str):
        lines = chunk.split("\n")
        spacing = len(str(len(lines)))
        return "\n".join([f"{i + 1:{spacing}d}  {lines[i]}" for i in range(len(lines))])
    
    def set_api_key(self, api_key: str):
        openai.api_key = api_key

    def lint(self, chunks, rules):
        prompt = self.prompt_template.format(
            rules="\n".join(rules), chunk=self.format_lines(chunks[0]["text"])
        )
        messages = [
            {"role": "system", "content": self.introduction},
            {"role": "user", "content": prompt},
        ]

        for message in messages:
            print(message["content"])

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=0,
            max_tokens=256,
            frequency_penalty=0,
            presence_penalty=0,
        )

        for choice in response["choices"]:
            print(choice["message"]["content"])

    introduction = textwrap.dedent(
        """
        You are AI Linter, an AI assistant to lint programming language code with English text rules.

        VIOLATION OUTPUT FORMAT:
        Code: <violated chunk>
        Line: <The line of the violation considering blank lines>
        Start column: <first character position in the line of the violation>
        End column: <last character position in the line of the violation>
        Rule: <The rule that was violated>
        Reason: <Why the rule was violated>

        EXAMPLE:
        \"\"\"
        USER:
        RULES:
        Variables, methods, and functions should be snake case

        Lint the following code
        ```python
         1  from typing import Sequence
         2
         3  from .commands.init import Init
         4  from .commands.run import Run
         5  from .command import Command
         6
         7
         8  commands: Sequence[Command] = [
         9      Init(),
        10      Run(),
        11  ]
        12  def someFunction(subparsers):
        13      for command in commands:
        14          command.configure(subparsers)
        ```

        ASSISTANT:
        Code: `someFunction`
        Line: 14
        Start column: 5
        End column: 22
        Rule: Variables, methods, and functions should be snake case
        Reason: `someFunction` isn't separating words by an underscore.
        \"\"\"

        The following procedure was used to lint the example code:
        Step 1: Analyse the rules from the "RULES" section.

        Variables, methods, and functions should be snake case
        - The rule checks for naming conventions, every variable, method, and function needs to separate words with the underscore character.

        Classes should be in pascal case
        - The rule checks for naming conventions, every class needs to have the initial letter of each word in uppercase

        Step 2: Analyse the code based on the rules.

        There's no way to know the type from the imports so it will be ignored

        `commands` is a variable, according to the rules it needs to be snake case, as a single world lower case it is snake case.

        `someFunction` is a function, according to the rules it needs to be snake case. The rules are violated as someFunction isn't separating words by an underscore.

        `command` is a variable, according to the rules it needs to be snake case,  as a single world lower case it is snake case.

        `configure` is a method, according to the rules it needs to be snake case, as a single world lower case it is snake case.

        Step 3:
        Code: `someFunction`
        Line: 14
        Start column: 5
        End column: 22
        Rule: Variables, methods, and functions should be snake case
        Reason: `someFunction` isn't separating words by an underscore.
        """
    )
