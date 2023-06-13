import argparse

from .commands import COMMANDS
from .version import get_version


def start_cli():
    parser = argparse.ArgumentParser(
        prog="AI Linter", description="The AI that lints your code"
    )
    subparsers = parser.add_subparsers()

    parser.set_defaults(func=lambda _: parser.print_help())
    parser.add_argument("--version", action="version", version=get_version())

    for command in COMMANDS:
        command.configure(subparsers)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    start_cli()
