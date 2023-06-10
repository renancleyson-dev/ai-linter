from typing import TypedDict, NotRequired

ParseParameter = TypedDict(
    "ParseParameter",
    {
        "chunk": str,
        "type": str,
        "line": str,
        "start-column": str,
        "end-column": str,
        "observation": NotRequired[str],
    },
)


__EXAMPLE_CODE = """\
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
15          command.some_method()
"""

__EXAMPLE_ANSWER = """\
"chunk","type","line","start-column","end-column","observation"
"Sequence","typing","1","20","28",
"Init","class","3","28","32",
"Run","class","4","27","30",
"Command","class","5","22","29",
"commands","variable","8","1","9","`commands` is a list"
"someFunction","function","12","5","17",
"subparsers","variable","12","18","28",
"command","variable","13","9","16",\
"""

INSTRUCTION_TEMPLATE = """\
You are AI Linter, an assistant for linting code with rules in English text.

Each rule has a category. Your task is to extract relevant parameters of the category \
"Naming convention" from a code chunk. For example, the code `foo = 5` has a relevant \
parameter to extract for naming convention, the `foo` variable.

You should extract the parameters identified with the following types:
    - variable
    - function
    - class
    - typing

Be aware that the code lines will be enumerated and the columns will be counted two \
whitespaces after the line number, for example `14      test = 5` has the columns \
represented with the following table:
|1|2|3|4|5|6|7|8|9|10|11|12|
|-|-|-|-|-|-|-|-|-|-|-|-|-|
| | | | |t|e|s|t| |=| |5|
"""

INPUT_TEMPLATE = """\
```{programming_language}
{chunk}
```\
"""

EXAMPLES = [
    {
        "question": INPUT_TEMPLATE.format(
            programming_language="python", chunk=__EXAMPLE_CODE
        ),
        "answer": __EXAMPLE_ANSWER,
    },
]
