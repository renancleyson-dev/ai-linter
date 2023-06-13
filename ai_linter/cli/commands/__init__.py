from ..command import Command
from .init import Init
from .run import Run

COMMANDS: list[Command] = [
    Init(),
    Run()
]