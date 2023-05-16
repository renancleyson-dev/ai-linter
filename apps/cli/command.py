from types import GenericAlias
from abc import ABC, abstractmethod, abstractclassmethod

"""
    Define Sub parser type
    from https://github.com/python/typeshed/issues/7539#issuecomment-1076640854
"""
import argparse
setattr(argparse._SubParsersAction, "__class_getitem__", classmethod(GenericAlias))
_SubparserType = argparse._SubParsersAction[argparse.ArgumentParser]


class Command(ABC):
    """
        Class for more composeable for CLI commands with argparse

        Basic Usage:

        ```
        class SomeCommand(Command):
            @classmethod
            def configure(cls, subparsers):
                # Add command to argparse
                parser = subparsers.add_parser('some command')
                # set run method to the command
                parser.set_defaults(func=cls().run)

            def run(self, args):
                print("running with", args)
        ```
    """

    @abstractmethod
    def run(self, args):
        """
            Use this method to run with argparse
            Example: subparser.setdefaults(func=CommandExample().run)
        """
        return NotImplemented

    @abstractclassmethod
    def configure(cls, subparsers: _SubparserType):
        """
            command configuration for argparse
        """
        return NotImplemented
