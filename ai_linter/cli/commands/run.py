import os
import pathlib
from glob import glob
from ai_linter.core.linter import Linter
from ai_linter.core.models import Repository
from ai_linter.core.storage.configuration_storage import Configuration
from ai_linter.core.utils.list_tools import flat

from ..command import Command
from ..settings import configuration_storage, lint_engine


class Run(Command):
    class Args:
        path: str

    def configure(self, subparsers):
        parser = subparsers.add_parser(
            "run",
            description="Run the linter. The conf file is required to be within the current folder",
        )
        parser.add_argument(
            "--path",
            help="path to lint, defaults to the current directory",
            default=os.getcwd(),
        )
        parser.set_defaults(func=self.run)

    def run(self, args: Args):
        abspath = os.path.abspath(args.path)
        configuration = configuration_storage.get_configuration(os.getcwd())
        api_key = configuration.get("OPENAI_API_KEY")

        if not configuration.get("rules"):
            raise ValueError("rules missing on the .ai-linter.json")

        if not api_key:
            raise ValueError("OPENAI_API_KEY missing on the .ai-linter.json")

        linter = Linter(configuration)
        lint_engine.set_api_key(api_key)

        if os.path.isdir(abspath):
            repository = self.open(abspath, configuration)
            print(linter.lint_by_repository(repository))
        elif os.path.isfile(abspath):
            print(linter.lint_by_file(abspath))
        else:
            raise ValueError("No such file or directory")

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
