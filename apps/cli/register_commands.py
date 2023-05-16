from typing import List
from command import Command
from commands.init import Init

commands: list[Command] = [
    Init,
]


def register_commands(subparsers):
    for command in commands:
        command.configure(subparsers)
