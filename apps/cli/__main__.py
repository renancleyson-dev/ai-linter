import argparse
from register_commands import register_commands
import version


def start_cli():
    parser = argparse.ArgumentParser(
        prog='AI Linter',
        description='The AI that lints your code')

    parser.set_defaults(func=lambda _: parser.print_help())
    parser.add_argument('--version', action='version', version=version.get_version())
    register_commands(parser.add_subparsers())

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    start_cli()
