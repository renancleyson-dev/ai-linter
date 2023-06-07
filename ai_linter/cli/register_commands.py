from typing import Sequence

from .commands.init import Init
from .commands.run import Run
from .command import Command


commands: Sequence[Command] = [
    Init(),
    Run(),
]


def register_commands(subparsers):
    for command in commands:
        command.configure(subparsers)
