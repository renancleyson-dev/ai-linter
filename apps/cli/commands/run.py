import os
import pathlib
from glob import glob

from core.linter import Linter

from ..command import Command
from core.common.models import Repository
from core.common.storage import Configuration
from ..config import ConfigurationStorage, LintEngine
from core.utils.list_tools import flat


class Run(Command):
    class Args:
        path: str

    def configure(self, subparsers):
        parser = subparsers.add_parser(
            "run", description="Run the linter into a codebase, directory, or file"
        )
        parser.add_argument(
            "--path",
            help="path to lint, defaults to the current directory",
            default=os.getcwd(),
        )
        parser.set_defaults(func=self.run)

    def run(self, args: Args):
        abspath = os.path.abspath(args.path)
        configuration = ConfigurationStorage.get_configuration(abspath)
        linter = Linter(configuration)

        if not configuration["rules"]:
            raise ValueError("rules missing on the .ai-linter.json")
        
        if not configuration["OPENAI_API_KEY"]:
            raise ValueError("OPEN_API_KEY missing on the .ai-linter.json")

        repository = self.open(abspath, configuration)

        LintEngine.set_api_key(configuration["OPENAI_API_KEY"])
        linter.lint_by_repository(repository)

    @staticmethod
    def get_directory(relative_dirpath: str, repository: Repository):
        root_path = pathlib.Path(repository.root.path)
        dirpath = os.path.join(root_path.parent, relative_dirpath)

        return repository.get_directory(dirpath)

    @staticmethod
    def get_exclude_paths(root_path: str, configuration: Configuration):
        exclude = configuration.get("exclude", [])
        paths_nested = [glob(p, recursive=True, root_dir=root_path) for p in exclude]

        return [os.path.join(root_path, p) for p in flat(paths_nested)]

    def open(self, root_path: str, configuration: Configuration) -> Repository:
        repository = Repository(root_path)
        extensions = configuration["extensions"]
        exclude_paths = self.get_exclude_paths(root_path, configuration)

        for dirpath, dirnames, files in os.walk(root_path):
            directory = self.get_directory(dirpath, repository)

            for dirname in dirnames:
                repository.add_directory(dirname, directory)

            for file_name in files:
                path = os.path.join(directory.path, file_name)
                if file_name.endswith(tuple(extensions)) and not path in exclude_paths:
                    repository.add_file(file_name, directory)

        return repository
