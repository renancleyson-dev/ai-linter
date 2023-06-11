from dataclasses import dataclass, field
from typing import Optional, TypedDict, Callable, Generic, TypeVar, NotRequired
from enum import Enum

TransformOutput = TypeVar("TransformOutput")


class Rules(str, Enum):
    NAMING_CONVENTION = "naming-convention"
    FORMATTING = "formatting"
    BEST_PRACTICE = "best-practice"
    MIGRATION = "migration"


class Example(TypedDict):
    question: str
    answer: str


class Error(TypedDict):
    message: str
    line: int
    start_column: int
    end_column: int
    fix: NotRequired[str]


@dataclass
class Prompt(Generic[TransformOutput]):
    input: str

    """
    Adding a parameter for the Transformer is required til PEP 696 is implemented
    in mypy.
    """
    parse: Callable[[str], TransformOutput]

    instruction: Optional[str] = None
    examples: list[Example] = field(default_factory=list)
