import os
import pathlib

from ..config import ConfigurationStorage
from ..command import Command


class Init(Command):
    class Args:
        path: str

    def configure(self, subparsers):
        parser = subparsers.add_parser(
            "init", description="Initialize linter into a codebase"
        )
        parser.add_argument(
            "--path",
            help="project directory to initialize codebase index",
            default=os.getcwd(),
        )
        parser.set_defaults(func=self.run)

    def run(self, args: Args):
        root_path = pathlib.Path(args.path)
        root_abspath = str(root_path.resolve())

        if not root_path.is_dir():
            raise ValueError(f"{root_abspath} isn't a directory")

        if ConfigurationStorage.has_configuration(root_abspath):
            raise RuntimeError("Project already initialized.")

        configuration = ConfigurationStorage.get_configuration(root_abspath)

        configuration["extensions"] = input(
            "Inform the file extensions to index separated by comma(.py, .js):\n"
        ).split(", ")

        exclude = input(
            "Inform any paths you want to ignore by comma(optional):\n"
        ).split(", ")

        exclude = [item for item in exclude if item]
        if exclude:
            configuration["exclude"] = exclude

        ConfigurationStorage.save_configuration(configuration, root_abspath)
