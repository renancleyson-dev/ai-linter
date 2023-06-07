from types import GenericAlias
from abc import ABC, abstractmethod

"""
    Define Sub parser type
    from https://github.com/python/typeshed/issues/7539#issuecomment-1076640854
"""
import argparse

setattr(argparse._SubParsersAction, "__class_getitem__", classmethod(GenericAlias))
_SubparserType = argparse._SubParsersAction[argparse.ArgumentParser]


class Command(ABC):
    """
    Class for more composeable CLI commands with argparse

    Basic Usage:

    ```
    class SomeCommand(Command):
        class Args:
            \"\"\"
            Type hints for parsed args
            \"\"\"
            test: str

        def configure(self, subparsers):
            parser = subparsers.add_parser('some command')
            parser = subparsers.add_parser('test', help="test arg")
            parser.set_defaults(func=self.run)

        def run(self, args: Args):
            print("running with", args)
    ```
    """

    @abstractmethod
    def run(self, args):
        """
        Use this method to run with argparse
        Example: subparser.setdefaults(func=CommandExample().run)
        """
        pass

    @abstractmethod
    def configure(self, subparsers: _SubparserType):
        """
        command configuration for argparse
        """
        pass
