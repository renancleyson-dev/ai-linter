from dataclasses import dataclass, field
from typing import Optional, TypedDict, Callable, Generic, TypeVar, NotRequired
from enum import StrEnum

TransformOutput = TypeVar("TransformOutput")


class Rules(StrEnum):
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
    parse: Callable[[str], TransformOutput]
    instruction: Optional[str] = None
    examples: list[Example] = field(default_factory=list)
