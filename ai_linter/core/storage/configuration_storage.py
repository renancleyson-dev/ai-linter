from abc import ABC, abstractmethod
from typing import TypedDict, NotRequired
import json
import os


class Rule(TypedDict):
    condition: str
    extensions: NotRequired[list[str]]


class Configuration(TypedDict):
    rules: list[Rule]
    extensions: list[str]
    exclude: NotRequired[list[str]]
    OPENAI_API_KEY: NotRequired[str]


class BaseConfigurationStorage(ABC):
    """
    The configuration is a dict.
    prefer to extend the key's value to avoid overriding previous configuration.
    """

    source: str

    @abstractmethod
    def has_configuration(self, source: str) -> bool:
        pass

    @abstractmethod
    def get_configuration(self, source: str) -> Configuration:
        pass

    @abstractmethod
    def save_configuration(self, configuration: Configuration, source: str):
        pass


class LocalConfigurationStorage(BaseConfigurationStorage):
    base_name = ".ai-linter.json"
    DEFAULT_CONFIGURATION: Configuration = {"rules": [], "extensions": []}

    def has_configuration(self, source):
        return os.path.exists(os.path.join(source, self.base_name))

    def get_configuration(self, source):
        if not self.has_configuration(source):
            return self.DEFAULT_CONFIGURATION

        with open(os.path.join(source, self.base_name)) as config_file:
            configuration: Configuration = json.load(config_file)
            return configuration

    def save_configuration(self, configuration: Configuration, source):
        with open(os.path.join(source, self.base_name), "w") as config_file:
            json.dump(configuration, config_file, indent=2)
